template <typename value_type>
class smart_ptr
{
    value_type * data;
    unsigned * cnt;
    void (*destr)(value_type * const);
    
    public:
    smart_ptr() : data(nullptr), cnt(nullptr), destr(nullptr) {};
    
    smart_ptr(value_type * const ptr, decltype(destr) destr_ptr = nullptr)
        : data(ptr), cnt(new unsigned(1)), destr(destr_ptr) {}
        
    smart_ptr(const value_type & data, decltype(destr) destr_ptr = nullptr) 
        : smart_ptr(new value_type(data), destr_ptr) {}
        
    smart_ptr(smart_ptr& ptr) 
        : data(ptr.data), cnt(ptr.cnt), destr(ptr.destr)
    {
        ++*cnt;
    }
    
    value_type& operator * () 
        {return *data;}
        
    void operator = (smart_ptr<value_type>& ptr) {
        this->~smart_ptr();
        data = ptr.data;
        cnt = ptr.cnt;
        ++*cnt;
        destr = ptr.destr;
    }
    
    void operator = (value_type * const ptr) {
        this->~smart_ptr();
        data = ptr;
        cnt = new unsigned(1);
        destr = nullptr;
    }
    
    operator bool()
        {return data;}
        
    ~smart_ptr()
    {
        if (!cnt)
            return;
        if (--*cnt == 0)
        {
            (destr) ? destr(data) : delete data;
            delete cnt;
        }
    }
};
