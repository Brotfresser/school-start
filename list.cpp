#include <initializer_list>

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
    };

    class iterator
    {
        friend list;

        node * now;
        iterator(node * now): now(now) {}
        iterator(value_type value, node * prev, node * next)
            : now(new node(value, prev, next)) {}

        public:
            inline bool operator == (const iterator & compared) const
                {return now == compared.now;}
            
            inline bool operator != (const iterator & compared) const
                {return !( *this == compared);}

            inline value_type & operator * () const
                {return * now->value;}

            inline iterator & operator++()
            {
                now = now->next;
                return *this;
            }
            
            inline iterator & operator++(int)
            {
                iterator temp (*this);
                ++*temp;
                return temp;
            }

            inline iterator & operator--()
            {
                now = now->prev;
                return * this;
            }
            
            inline iterator & operator --(int)
            {
                iterator temp (*this);
                --*temp;
                return temp;
            }
    };

    private:
        node * begin_node;
        node * end_node = new node();
        unsigned int list_size = 1;
    public:

    ~list()
    {
        node * del_node = begin_node;
        node * next_node = begin_node -> next;

        for (int i = 0; i < list_size; ++i)
        {
            delete del_node;
            del_node = next_node;
            next_node = next_node -> next;
        }
        delete end_node;

    }

    inline void default_nodes_init() const
    {
        begin_node->prev = begin_node->next = end_node;
        end_node->prev = begin_node;
    }
    
    list() : begin_node(new node(value_type())) {default_nodes_init();}
    
    list(std::initializer_list<value_type> args) : begin_node(nullptr)
    {
        auto arg = args.begin();
        begin_node = new node(*arg++);
        default_nodes_init();
        
        for (; arg != args.end(); ++arg)
            push_back(*arg);
            
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
    {
        iterator new_iter = insert(end(), value);
        return new_iter;
    }
};
