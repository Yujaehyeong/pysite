import math

from django.db import models

# Create your models here.
from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    hit = models.IntegerField(default=0)
    regdate = models.DateTimeField(auto_now=True)
    groupno = models.IntegerField(default=0)
    orderno = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user = models.ForeignKey(User, to_field='id', on_delete=models.CASCADE)
    # on_delete= 유저가 지워지면 어떻게할것인지 정의


class Paging:
    def __init__(self):
        self.page_count = 5
        self.block_start_num = 0
        self.block_last_num = 0
        self.start_page_num = 0
        self.last_page_num = 0
        self.cur_page_num=0

    def makelastpageNum(self, total_board_count, show_board_num):
        total = total_board_count
        if total % show_board_num == 0:
            self.last_page_num = math.trunc(total/show_board_num)
        else:
            self.last_page_num = math.trunc(total/show_board_num) + 1


    def makeblock(self, cur_page_num) :
        block_num = 0
        block_num = math.trunc((cur_page_num - 1)/ self.page_count)
        self.block_start_num = (block_num * self.page_count) + 1
        self.block_last_num =  self.block_start_num + (self.page_count - 1)

        if self.block_last_num<self.last_page_num:
            self.block_last_num= self.block_last_num
        else:
            self.block_last_num =  self.last_page_num

    def makestartpagenum(self, show_board_num) :
        self.start_page_num = (self.cur_page_num -1)*show_board_num;

    def pagingsetting(self, total_board_count, show_board_num, cur_page_num):
        self.makelastpageNum(total_board_count, show_board_num);
        self.cur_page_num = cur_page_num;
        self.makeblock(cur_page_num);
        self.makestartpagenum(show_board_num);

    def __str__(self):
        return f'Board({self.page_count}, {self.block_start_num},{self.block_last_num},\
         {self.start_page_num},  {self.last_page_num},  {self.cur_page_num})'