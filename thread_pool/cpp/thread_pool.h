/*************************************************************************
	> File Name: thread_pool.h
	> Author: 
	> Mail: 
	> Created Time: Fri 27 Mar 2014 02:21:02 PM CST
 ************************************************************************/

#ifndef _THREAD_POOL_H
#define _THREAD_POOL_H

#include <boost/shared_ptr.hpp>

struct ThreadTask{
    boost::function<void ()> task_function_;
    void *args;
};

/**
 *
 **/
class TreadPool{
 public:
  TreadPoll();
  ~TreadPoll();
 private:
  bool is_stop_;
  uint32_t work_thread_max_;
  uint32_t work_thread_min;
  uint32_t work_thread_num;
  std::queue<boost::shared_ptr<boost::TreadTask> > task_queue_;
  std::vector<boost::shared_ptr<boost::thread> >   work_thread_;
};

#endif
