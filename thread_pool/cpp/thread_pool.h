/*************************************************************************
	> File Name: thread_pool.h
	> Author: 
	> Mail: 
	> Created Time: Fri 27 Mar 2014 02:21:02 PM CST
 ************************************************************************/

#ifndef _THREAD_POOL_H
#define _THREAD_POOL_H

#include <vector>
#include <memory>       // For std::shared_ptr
#include <thread>
#include "blocking_queue.h"

/**
 * Define a task
 **/
struct ThreadTask{
    std::function<void ()> task_function_;
    void *args;
};

const uint32_t kWorkThreadNum = 128;
/**
 * Define a thread pool
 **/
class ThreadPool{
 public:
  // Construction
  ThreadPool(const uint32_t thread_num = kWorkThreadNum):
    is_stop_(false),work_thread_num_(thread_num){
      if(!is_stop_){
        start();
      }
    }

  // Destruction
  ~ThreadPool(){
    is_stop_ = true; 
    stop();
  }

  void add_task(const ThreadTask& task);
 private:
  // start thread
  void start();

  // stop thread
  void stop();
  // Run a task
  void run();

  bool is_stop_;
  uint32_t work_thread_max_;
  uint32_t work_thread_min_;
  uint32_t work_thread_num_;
  CBlockingQueue<ThreadTask> task_queue_;
  std::vector<std::shared_ptr<std::thread> >   work_thread_;
};

#endif
