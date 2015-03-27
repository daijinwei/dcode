/*************************************************************************
	> File Name: blocking_queue.h
	> Author: 
	> Mail: 
	> Created Time: Fri 27 Mar 2015 04:33:32 PM CST
 ************************************************************************/

#ifndef _BLOCKING_QUEUE_H
#define _BLOCKING_QUEUE_H

#include <deque>
#include <mutex.h>

/* Define max item num */
const uint32_t kMaxItem = static_cast<uint32_t>(-1)

template<typename Item>
class CBlockingQueue {
 public:
  CBlockingQueue(uint32_t max_item = kMaxItem){
    assert(kMaxItem > 0);
  }
  ~CBlockingQueue();
  bool push_front(const Item& item){
    bool ret = false;
    std::unique_lock(std::mutex) lock(mutex_);
    if(!unlock_is_full_()){
      dqueue_.push_front(item);
      ret = true;
    }
    lock.unlock();
    not_empty_condition_.notify_one();

    return ret;
  }
  bool push_back(const Item& item){
    bool ret = false;
    std::unique_lock(std::mutex) lock(mutex_);
    if(!unlock_is_full_()){
      dqueue_.push_back(item);
      ret = true;
    }
    lock.unlock();
    not_empty_condition_.notify_one();

    return ret;
  }
        
  void pop_front(Item &item){
    std::unique_lock(std::mutex) lock(mutex_);
    while(unlock_is_empty()){
        not_empty_condition_wait(lock); 
    }
    item = dqueue_.front();
    dqueue_.pop_front();
    lock.unlock();
    not_full_condition_.notify_one();
  }

  void pop_back(Item item){
    std::unique_lock(std::mutex) lock(mutex_);
    while(unlock_is_empty()){
        not_empty_condition_wait(lock); 
    }
    item = dqueue_.back();
    dqueue_.pop_back();
    lock.unlock();
    not_full_condition_.notify_one();
  }

  bool is_full() const{
    return unlock_is_full();       
  }

  uint32_t size() const{
    return dqueue_.size();
  }

 private:
  bool unlock_is_full() const{
    return dqueue_.size() >= queue_max_item;
  }
  bool unlock_is_empty(){
    return dqueue_.empty();
  }
  uint32_t  queue_max_item;
  std::mutex  mutex_;
  std::condition_variable not_empty_condition_;
  std::condition_variable not_full_condition_;

  std::deque<Item>     dqueue_;
};

#endif
