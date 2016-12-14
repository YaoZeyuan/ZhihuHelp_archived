# -*- coding: utf-8 -*-
class Book(object):
    u"""
    正式用于渲染书籍的容器
    """
    def __init__(self, task_result_list):
        self.task_result_list = task_result_list

        self.is_split = False   # 是否是被拆分后的结果集
        self.chapter_no = 0     # 若是被拆分后的结果集，那么是哪一集
        return

    def auto_split(self, max_size_page_kb=50 * 1024):
        if max_size_page_kb < 1 * 1024:
            #   不能任意小啊
            max_size_page_kb = 1 * 1024
        if self.get_total_img_size_kb() <= max_size_page_kb:
            #   大小符合要求，最好
            return [self]

        if not self.is_split:
            # 第一次分隔，序号应该为卷1
            self.is_split = True
            self.chapter_no = 1

        #   文章和问题分别对待，方便处理
        new_book = Book([])
        new_book.is_split = True
        new_book.chapter_no = self.chapter_no + 1

        while self.get_total_img_size_kb() > max_size_page_kb:
            task_result = self.task_result_list.pop()
            if len(self.task_result_list) == 0:
                # 最后一个任务
                legal_task_result, remain_task_result = task_result.auto_split(max_size_page_kb)
                self.task_result_list.append(legal_task_result)
                new_book.task_result_list.insert(0, remain_task_result)
                return [self] + new_book.auto_split(max_size_page_kb)
            else:
                new_book.task_result_list.insert(0, task_result)
        return [self] + new_book.auto_split(max_size_page_kb)

    def get_total_img_size_kb(self):
        total_img_size_kb = 0
        for task_result in self.task_result_list:
            total_img_size_kb += task_result.get_total_img_size_kb()
        return total_img_size_kb


