#include <initializer_list>

// мб нодам хранить их индекс, чтобы можно было сравнивать итераторы? (iter_l < iter_r ? : throw out_of_range("you stupid bastartd!"))

template <typename value_type>
struct list
{
    class node
    {
        friend list;

        node * prev = nullptr;
        node * next = nullptr;
        value_type * value = nullptr;

        node() = default;
        node(value_type value): value(new value_type(value)) {}
        node(value_type value, node * prev, node * next)
            : value(new value_type(value)), prev(prev), next(next) {}
        node(node& copy) : node(copy.value, copy.prev, copy.next) {}
    };

    class iterator
    {
        friend list;

        node * now;
        iterator(node * now): now(now) {}
        iterator(value_type value, node * prev, node * next)
            : now(new node(value, prev, next)) {}
        iterator(const iterator& copy) 
            : iterator(copy.now) {}

        public:
            inline bool operator == (const iterator & compared) const
                {return now == compared.now;}
            
            inline bool operator != (const iterator & compared) const
                {return !( *this == compared);}

            inline value_type & operator * () const
                {return *now->value;}

            inline iterator & operator++()
            {
                now = now->next;
                return *this;
            }
            
            inline iterator operator++(int)
            {
                iterator temp (*this);
                ++*this;
                return temp;
            }

            inline iterator & operator--()
            {
                now = now->prev;
                return *this;
            }
            
            inline iterator operator --(int)
            {
                iterator temp (*this);
                --*this;
                return temp;
            }
    };

    private:
    void bind_nodes(node * first, node * second)
        {first->next = second; second->prev = first;}

        node * begin_node;
        node * end_node = new node();
        unsigned int list_size = 1;
    public:

    ~list()
    {
        node * del_node = begin_node;
        node * next_node = begin_node->next;

        while (next_node != end_node)
        {
            delete del_node;
            del_node = next_node;
            next_node = next_node->next;
        }
        delete end_node;

    }

    inline void default_nodes_init() const
    {
        begin_node->prev = begin_node->next = end_node;
        end_node->prev = begin_node;
    }
    
    list() : begin_node(new node(value_type())) 
        {default_nodes_init();}
    
    list(std::initializer_list<value_type> args) : begin_node(nullptr)
    {
        auto iter = args.begin();
        begin_node = new node(*iter++);
        default_nodes_init();

        push_back_range(iter, args.end());
    }

    list(const list& copy) : begin_node(nullptr)
    {
        auto iter = copy.begin();
        begin_node = new node(*iter++);
        default_nodes_init();

        push_back_range(iter, copy.end());
    }

    list& operator = (const list& copy)
    {
        auto iter_l = begin(), iter_r = copy.begin();
        for (; iter_l != end() && iter_r != copy.end(); ++iter_l, ++iter_r)
            *iter_l = *iter_r;
            
        if (size() < copy.size())
        {
            for (; iter_r != copy.end(); ++iter_r)
                push_back(*iter_r);
        }
        else if (size() > copy.size())
        {
            /*
            node* last_node = iter_l.now->prev;
            while (iter_l != end())
                delete iter_l++.now;
            bind_nodes(last_node, end_node);
            list_size = copy.size();
            */
           delete_range(iter_l, end());
        }
        return *this;
    }

    value_type operator [](int index) const
    {
        if (index == 0) return *begin();

        auto iter = begin();
        if (index > 0)
            for (int _ = 0; _ < index; ++_, ++iter);
        else
            for (int _ = -1; _ < -index; ++_, --iter);
        return *iter;
    }

    inline auto begin() const
        {return iterator(begin_node);}

    inline auto end() const
        {return iterator(end_node);}

    inline auto size() const
        {return list_size;}

    iterator insert(const iterator & pos, const value_type & value)
    {
        ++list_size;
        iterator new_iter(value, pos.now->prev, pos.now);
        pos.now->prev->next = new_iter.now;
        pos.now->prev = new_iter.now;
        
        return new_iter;
    }

    iterator push_front(const value_type & value)
    {
        iterator new_iter = insert(begin(), value);
        begin_node = new_iter.now;
        
        return new_iter;
    }

    iterator push_back(const value_type & value)
        {return insert(end(), value);}

    template <typename _Iterator>
    void delete_range(_Iterator iter_l, const _Iterator& iter_r)
    {
        int new_size = size();
        node * first_bind_node = (iter_l.now == begin_node ? new node(value_type()) : iter_l.now->prev);
        node * last_bind_node = (iter_r.now == end_node ? end_node : iter_r.now->next);

        for (; iter_l != iter_r; --new_size)
            delete iter_l++.now;

        bind_nodes(first_bind_node, last_bind_node);
        list_size = (new_size == 0 ? 1 : new_size);
    }

    template <typename _Iterator>
    void push_back_range(_Iterator iter, const _Iterator& end_iter)
    {
        for (; iter != end_iter; ++iter)
            push_back(*iter);
    }

    void print_nodes()
    {
        int i = 0;
        for (auto iter = begin(); iter != end(); ++iter, ++i)
            print(i, iter.now);
        print(i, end_node);
    }
};
