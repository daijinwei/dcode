/**
 * Copyright (c) 2015, project
 * File Name: thread_pool.cpp
 * Author: David<daijinwei41@gmail.com>
 * Created: 2015-03-28
 * Modified: 2015-03-28
 * Description: 
 **/

#include <assert.h>
#include "thread_pool.h"

void ThreadPool::add_task(const ThreadTask& task){
  if(!is_stop_){
    task_queue_.push_back(task);
  }
}

void ThreadPool::start(){
  assert(work_thread_num_ > 0);
  for(uint32_t count = 0; count != work_thread_num_; ++count){
    std::shared_ptr<std::thread> thread(new std::thread(&ThreadPool::run, this));
    work_thread_.push_back(thread);
  }
}

void ThreadPool::run(){
  while(!is_stop_){
    ThreadTask task; 
    task_queue_.pop_front(task);
    task.task_function_();
  } 
}
void ThreadPool::stop(){
  for(uint32_t count = 0; count != work_thread_.size(); ++count){
    if(!work_thread_.empty()){
      if(work_thread_.at(count)->joinable()){
        work_thread_.at(count)->join();
      }
    }
  }
}
