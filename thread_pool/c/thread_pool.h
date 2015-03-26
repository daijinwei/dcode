/*************************************************************************
	> File Name: thread_pool.h
	> Author: 
	> Mail: 
	> Created Time: Thu 26 Mar 2015 09:30:02 PM CST
 ************************************************************************/

#ifndef _THREAD_POOL_H
#define _THREAD_POOL_H

/**
 * Define a task 
 * TpTask: thread_pool_task
 * */

typedef struct TpTask TpTask

typedef void(*process_task)();

struct TpTaskDescription{
    void *args;         
    void *function;
}; 



#endif
