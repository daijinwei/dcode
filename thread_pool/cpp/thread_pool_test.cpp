/**
 * Copyright (c) 2015, project
 * File Name: thread_pool_test.cpp
 * Author: David<daijinwei41@gmail.com>
 * Created: 2015-03-28
 * Modified: 2015-03-28
 * Description: 
 **/

#include<iostream>
#include "thread_pool.h"

struct task_info{
    int x;
    int y;
};

void print_num(const struct task_info & info){
    std::cout << "x\t" << info.x << std::endl;
    std::cout << "y\t" << info.y << std::endl;
}

int main(){
    ThreadPool tp(128);
    for(int i = 0; i < 1000; i++){
        ThreadTask task;
        struct task_info info;
        info.x = i;
        info.y = i*i;
        task.task_function_ = std::bind(print_num, info);
        tp.add_task(task);
    }
}
