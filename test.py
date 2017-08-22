# coding=utf-8
import sys
import threading
import Queue
import traceback


class NoResultsPending(Exception):
    """
    All works requests have been processed
    """
    pass


class NoWorkersAvailable(Exception):
    """
    No worker threads available to process remaining requests.
    """
    pass


def _handle_thread_exception(request, exc_info):
    """
    默认的异常处理函数，只是简单的打印
    :param request:
    :param exc_info:
    :return:
    """
    traceback.print_exception(*exc_info)


class WorkerThread(threading.Thread):
    """
    后台线程，真正的工作线程，从请求队列(requestQueue)中获取work，
    并将执行后的结果添加到结果队列(resultQueue)
    """
    def __init__(self, p_request_queue, p_result_queue, p_poll_timeout=5, **kwds):

        threading.Thread.__init__(self, **kwds)

        # 设置为守护进行
        self.setDaemon(True)

        # 请求队列
        self._request_queue = p_request_queue

        # 结果队列
        self._result_queue = p_result_queue

        # 超时时间
        self._poll_timeout = p_poll_timeout

        # 设置一个flag信号，用来表示该线程是否还被dismiss,默认为false
        self._dismissed = threading.Event()

        # 开始执行
        self.start()

    def run(self):
        """
        每个线程尽可能多的执行work，所以采用loop，
        只要线程可用，并且requestQueue有work未完成，则一直loop
        :return:
        """
        while True:

            if self._dismissed.is_set():
                break

            try:
                # Queue.Queue队列设置了线程同步策略，并且可以设置timeout。 一直block，直到requestQueue有值，或者超时
                request = self._request_queue.get(True, self._poll_timeout)

            except Queue.Empty:
                continue

            else:
                # 之所以在这里再次判断dismissed，是因为之前的timeout时间里，很有可能，该线程被dismiss掉了
                if self._dismissed.is_set():
                    self._request_queue.put(request)
                    break

                try:
                    # 执行callable，讲请求和结果以tuple的方式放入requestQueue
                    result = request.callable(*request.args, **request.kwds)
                    print self.getName()
                    self._result_queue.put((request, result))

                except:
                    # 异常处理
                    request.exception = True
                    self._result_queue.put((request, sys.exc_info()))

    def dismiss(self):
        """
        设置一个标志，表示完成当前work之后，退出
        :return:
        """
        self._dismissed.set()


class WorkRequest:
    """
    请求
    """
    def __init__(self, p_callable_, p_args=None, p_kwds=None, p_request_id=None,
                 p_callback=None, p_exc_callback=_handle_thread_exception):
        """
        :param p_callable_: 可定制的，执行work的函数
        :param p_args: 列表参数
        :param p_kwds: 字典参数
        :param p_request_id: id
        :param p_callback: 可定制的，处理resultQueue队列元素的函数
        :param p_exc_callback: 可定制的，处理异常的函数
        :return:
        """
        if p_request_id is None:
            self.request_id = id(self)
        else:
            try:
                self.request_id = hash(p_request_id)
            except TypeError:
                raise TypeError("requestId must be hashable")

        #
        self.exception = False

        #
        self.callback = p_callback

        #
        self.exc_callback = p_exc_callback

        #
        self.callable = p_callable_

        #
        self.args = p_args or []

        #
        self.kwds = p_kwds or {}

    def __str__(self):
        return "WorkRequest id=%s args=%r kwargs=%r exception=%s" % \
               (self.request_id, self.args, self.kwds, self.exception)


class ThreadPool:
    """
    线程池
    """
    def __init__(self, p_num_workers, p_size=0, p_res_size=0, p_poll_timeout=5):
        """
        :param p_num_workers: 初始化的线程数量
        :param p_size: request 队列的初始大小
        :param p_res_size: result 队列的初始大小
        :param p_poll_timeout:
        :return:
        """
        #
        self._request_queue = Queue.Queue(p_size)

        #
        self._result_queue = Queue.Queue(p_res_size)

        #
        self.workers = []

        #
        self.dismissed_workers = []

        # 设置个字典，方便使用
        self.work_requests = {}

        #
        self.create_workers(p_num_workers, p_poll_timeout)

    def create_workers(self, num_workers, poll_timeout=5):
        """
        创建num_workers个WorkThread,默认timeout为5
        :param num_workers:
        :param poll_timeout:
        :return:
        """
        for i in range(num_workers):
            self.workers.append(WorkerThread(self._request_queue, self._result_queue, p_poll_timeout=poll_timeout))

    def dismiss_workers(self, num_workers, do_join=False):
        """
        停用num_workers数量的线程，并加入dismiss_list
        :param num_workers:
        :param do_join:
        :return:
        """
        dismiss_list = []
        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismiss_list.append(worker)
        if do_join:
            for worker in dismiss_list:
                worker.join()
        else:
            self.dismissed_workers.extend(dismiss_list)

    def join_all_dismissed_workers(self):
        """
        join 所有停用的thread
        :return:
        """
        # print len(self.dismissedWorkers)
        for worker in self.dismissed_workers:
            worker.join()
        self.dismissed_workers = []

    def put_request(self, request, block=True, timeout=None):
        """

        :param request:
        :param block:
        :param timeout:
        :return:
        """
        assert isinstance(request, WorkRequest)
        assert not getattr(request, 'exception', None)

        # 当queue满了，也就是容量达到了前面设定的p_size,它将一直阻塞，直到有空余位置，或是timeout
        self._request_queue.put(request, block, timeout)
        self.work_requests[request.request_id] = request

    def poll(self, block=False):
        """

        :param block:
        :return:
        """
        while True:

            if not self.work_requests:
                raise NoResultsPending
            elif block and not self.workers:
                raise NoWorkersAvailable
            else:
                pass

            try:
                # 默认只要resultQueue有值，则取出，否则一直block
                request, result = self._result_queue.get(block=block)

                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)

                if request.callback and not (request.exception and request.exc_callback):
                    request.callback(request, result)

                del self.work_requests[request.request_id]

            except Queue.Empty:
                break

    def wait(self):
        """

        :return:
        """
        while True:
            try:
                self.poll(True)
            except NoResultsPending:
                break

    def worker_size(self):
        """

        :return:
        """
        return len(self.workers)

    def stop(self):
        """
        join 所有的thread,确保所有的线程都执行完毕
        :return:
        """
        self.dismiss_workers(self.worker_size(), True)
        self.join_all_dismissed_workers()


if __name__ == '__main__':

    import random
    import time
    import datetime

    def do_work(data):
        time.sleep(random.randint(1,3))
        res = str(datetime.datetime.now()) + "" +str(data)
        return res

    def print_result(request,result):
        print "---Result from request %s : %r" % (request.request_id, result)

    main = ThreadPool(3)
    for i in range(40):
        req = WorkRequest(do_work, p_args=[i], p_kwds={}, p_callback=print_result)
        main.put_request(req)
        print "work request #%s added." % req.request_id

    print '-' * 20, main.worker_size(), '-' * 20

    counter = 0
    while True:
        try:
            time.sleep(0.5)
            main.poll()

            if counter == 5:
                print "Add 3 more workers threads"
                main.create_workers(3)
                print '-' * 20, main.worker_size(), '-' * 20

            if counter == 10:
                print "dismiss 2 workers threads"
                main.dismiss_workers(2)
                print '-' * 20, main.worker_size(), '-' * 20

            counter += 1

        except NoResultsPending:
            print "no pending results"
            break

    main.stop()

    print "Stop"
