template <typename value_type>
class smart_ptr
{
    value_type * data;
    unsigned * cnt;
    
    public:
    
    smart_ptr(const value_type & data) 
        : data(new value_type(data)), cnt(new unsigned(1)) {print("&")}
    
    smart_ptr(value_type && data)
        : data(new value_type(data)), cnt(new unsigned(1)) {print("&&")}
        
    smart_ptr(smart_ptr& ptr) 
        : data(ptr.data) 
    {
        cnt = ptr.cnt; 
        ++*cnt;
    }
    
    value_type& operator * () 
        {return *data;}
        
    ~smart_ptr()
    {
        if (--*cnt == 0)
        {
            delete data;
            delete cnt;
        }
    }
};
