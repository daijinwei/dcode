/**
 * Copyright (c) 2015, project
 * File Name: cache.h
 * Author: David<daijinwei41@gmail.com>
 * Created: 2014-03-29
 * Modified: 2014-03-29
 * Description: 
 **/

#ifndef _CACHE_LUR_H
#define _CACHE_LUR_H

#include <stdint.h>
#include <cassert>
#include <list>
#include <map>

const uint32_t kCacheSize = 1024;

template<typename Key, typename Value>
class LruCache{
public:
    typedef Key KeyType;
    typedef Value ValueType;
    typedef std::list<KeyType> KeyList;
    typedef typename KeyList::iterator KeyListIterator;
    typedef std::map<KeyType, std::pair<ValueType, KeyListIterator> > KeyMap;
    typedef typename KeyMap::iterator KeyMapIterator;

    LruCache(uint32_t cache_size = kCacheSize): 
    cache_map_size_(kCacheSize){}
    ~LruCache(){}
    // Retrun if find a object, else insert a new key to cache map
    ValueType&
    operator()(const KeyType& key){
        assert(!cache_map_.empty());
        KeyMapIterator it = cache_map_.find(key);
        // Find a key in cache
        if(it != cache_map_.end()){
            // Flush key postion, move the key to back cache_entry_.
            cache_entry_.splice(cache_entry_.end(),
                                cache_entry_,
                                (it->second)->second);
            return (it->second)->first;
        } else { // Insert a new key to cache
            ValueType value = key_to_value(key); 
            insert(key, value);
            return value;
        }
    }
private:
    void insert(const Key& key, const Value& value){
        if(cache_map_.size() >= cache_map_size_){
            clear_old_key(); 
        }else{
            cache_entry_.push_back(key);
            KeyListIterator it = cache_entry_.end();
            cache_map_.insert(key, make_pair(value, it));
        }
    }
    void clear_old_key(){
        assert(!cache_map_.empty());
        KeyType key = cache_entry_.front();
        cache_map_.erase(key);

        assert(!cache_entry_.empty());
        cache_entry_.pop_front();
    }
    ValueType (*key_to_value)(const KeyType& key); 

    size_t  cache_map_size_;
    KeyMap  cache_map_;
    KeyList cache_entry_; 
};

#endif
