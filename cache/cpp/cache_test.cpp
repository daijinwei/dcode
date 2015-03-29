/**
 * Copyright (c) 2015, project
 * File Name: cache_test.cpp
 * Author: David<daijinwei41@gmail.com>
 * Created: 2014-03-29
 * Modified: 2014-03-29
 * Description: 
 **/

#include<iostream>
#include "cache_lru.h"

using namespace std;

std::string function(const std::string &s){
    std::string str;
    str = s;
    return str;
}
int main(){
    LruCache<std::string,std::string> cache_map(function, 100);
}
