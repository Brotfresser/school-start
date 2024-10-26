// TODO: переписать iterator в node

#include <iostream>
#include <initializer_list>

using std::endl;
#define print(x) std::cout << x << endl;
#define forlist(lst) for(int i = 0; i < lst.size(); ++i)

template <typename value_type>
struct list
{
    class iterator
    {
        friend list;
        
        iterator() = default;
        
        iterator(value_type var, iterator * left, iterator * right) 
            : prev(left), next(right), value(new value_type(var)), now(this) {}
        
        iterator(iterator * left, iterator * right)
            : iterator(value_type(), left, right) {}
            
        value_type * value = new value_type();
        iterator * prev = nullptr;
        iterator * next = nullptr;
        
        // атавизм от дебагинга, можно убрать, но придётся переделывать ==()
        // begin()/end() передают копию итератора, так что now это типа указатель на итератор, на который ссылается копия
        iterator * now = nullptr;
        
        public:
        inline void show() const
        {
            std::cout << prev << " < " << now << " | "
            <<  *value << " > " << next << endl;
        }
        
        iterator& operator ++ ()
        {
            prev = next->prev;
            now = next->now;
            value = next->value;
            next = next->next;
            
            return *this;
        }
        
        iterator operator ++ (int)
        {
            iterator temp(*this);
            ++*this;
            return temp;
        }
        
        iterator& operator -- ()
        {
            next = prev->next;
            now = prev->now;
            value = prev->value;
            prev = prev->prev;
            
            return *this;
        }
        
        iterator operator -- (int)
        {
            iterator temp(*this);
            --*this;
            return temp;
        }
        
        inline value_type& operator * ()
            {return *value;}
        
        inline bool operator == (const iterator& another) const
            {return now == another.now;}
            
        inline bool operator != (const iterator& another) const
            {return !(*this == another);}
    };
    
    private:
        iterator * pstart_iter = new iterator;
        iterator * pend_iter = new iterator;
        unsigned int list_size = 2;
    public:
    
    bool debug_mode = true;
    
    list() {default_init();}
    
    list(std::initializer_list<value_type> args) : list()
{
        auto iter = begin();
        if (args.size() > 2)
        {
            auto arg = args.begin();
            for (int i = 0; i < 2; ++i, ++iter, ++arg)
               *iter = *arg;
            for (int i = 2; i < args.size(); ++i, ++iter, ++arg)
                push_back(*arg);
        }
        else
            for (auto arg : args)
                *(iter++) = arg;
    if (debug_mode)
        print("\n\tend of list_constructor\n")
}

/*
    list(bool is_debug_mode, std::initializer_list<value_type> args)
: list(args)
{debug_mode = is_debug_mode;}
*/

    inline iterator begin()
    {return iterator(*pstart_iter);}
    
    inline iterator end()
    {return iterator(*pend_iter);}
    
    inline unsigned int size()
    {return list_size;}
    
    
    void default_init()
    {
        if (debug_mode)
        {
            std::cout << "start > " << pstart_iter << ' ' << *pstart_iter->value;
            std::cout << " | end > " << pend_iter << ' ' << *pend_iter->value << endl;
        }
        
        pstart_iter->next = pstart_iter->prev = pend_iter; 
        pstart_iter->now = pstart_iter;
        
        pend_iter->next = pend_iter->prev = pstart_iter; 
        pend_iter->now = pend_iter;
    }
    
    
    ~list()
    {
        print(debug_mode)
        if (debug_mode)
            print("start of destructor")
        iterator * del_iter = pstart_iter;
        iterator * next_iter = pstart_iter->next;
        
        if (debug_mode)
            print("start of for()")
        for (int _= 0; _ < list_size; ++_)
        {
            if (debug_mode)
                std::cout  << "was deleted " << del_iter <<endl;
                
            delete del_iter;
            del_iter = next_iter;
            next_iter = next_iter->next;
        }
    }
    
    /*
    iterator linsert(iterator& place, const value_type& value)
    {
        ++list_size;
        iterator * pnew_iter = new iterator(value, place.prev, &place);
        place.prev->next = pnew_iter;
        place.prev = pnew_iter;
        
        if (debug_mode)
            std::cout<< "new liter > " << pnew_iter<< " | " << *pnew_iter->value <<endl;
            
        return iterator(*pnew_iter);
    }*/
    
    iterator rinsert(iterator& place, const value_type& value)
    {
        ++list_size;
        iterator * pnew_iter = new iterator(value, place.next->prev, place.next);
        place.next->prev = pnew_iter;
        place.next = pnew_iter;
        
        if (debug_mode)
        {
            std::cout<<"new riter > " << pnew_iter << " | " << *pnew_iter->value <<endl;
            print(1)
            pnew_iter->show();
        }    
        return iterator(*pnew_iter);
    }
    
    iterator push_back(const value_type& value)
    {
        ++list_size;
        iterator * pnew_iter = new iterator(value, pend_iter, pstart_iter);
        
        if (debug_mode)
            std::cout<< "new iter > " << pnew_iter << " | " << *pnew_iter->value <<endl;
        
        pend_iter->next = pstart_iter->prev = pnew_iter;
        pend_iter = pnew_iter;
        return iterator(*pnew_iter);
    }
};


int main(int argc, char *argv[])
{
	list<int> a{1,2,3,4,5,6,7};
	   
	auto it = a.begin();
	++it; ++it;
	it.show();
	a.rinsert(it, 100);
	
	print("end of code, let's show values!")
	for (auto iter = a.begin(); iter != a.end(); ++iter)
	    print(*iter)
	print("it's trully end of code")
}
