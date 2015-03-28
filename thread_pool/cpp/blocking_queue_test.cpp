/*************************************************************************
	> File Name: blocking_queue_test.cpp
	> Author: 
	> Mail: 
	> Created Time: Fri 27 Mar 2014 06:07:58 PM CST
 ************************************************************************/

#include <iostream>
#include "blocking_queue.h"

int main(){
  CBlockingQueue<uint32_t> queue;
  queue.push_back(1);
  queue.push_back(2);
  queue.push_back(3);
  queue.push_back(4);
  queue.push_back(5);

  uint32_t n;
  queue.pop_front(n);
  std::cout << "n\t" << n << std::endl;

  queue.pop_front(n);
  std::cout << "n\t" << n << std::endl;

  queue.pop_front(n);
  std::cout << "n\t" << n << std::endl;

  queue.pop_front(n);
  std::cout << "n\t" << n << std::endl;

  queue.pop_front(n);
  std::cout << "n\t" << n << std::endl;
  // Should be blocking
  queue.pop_front(n);
  std::cout << "n\t" << n << std::endl;
}
