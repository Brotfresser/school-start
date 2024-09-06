#include <iostream>
#include <vector>
#include <string>
#include <cctype>
//#include "randint.cpp"
#ifndef MY_RANDINT
#include <random>
#endif


using std::endl; using std::cin;
using vector_2d = std::vector<std::vector<int>>;
#define print(x) std::cout << x << std::endl;


void print_screen(bool show_all=false);
void open_cell(int x, int y, vector_2d & checked_cells);
void vector_2d_init(vector_2d&);
void global_map_init(int empty_x=-1, int empty_y=-1);
int randint(int start_num, int end_num);
void clear_cin();


vector_2d global_map, player_map; // сначала у, потом х
std::vector<std::string> congrats {"МОЛОДЕЦ!", "Красава", "Так держать!", "ТЫ ПОБЕДИЛ!", "ВСех РазнёС!", "уничтожил!", "ЛОЛ"};
int SIZE_Y, SIZE_X, mines_cnt;
enum {HERE_BOMB = -1, CLOSED_CELL, OPENED_CELL, HERE_SHOULD_BE_BOMB, MAYBE_HERE_BOMB};
bool debug_mode = false;
int moves_done, flags_marked, right_flags_marked;

//TODO отрисовка x на карте
int main(){
    new_game:
    SIZE_Y = SIZE_X = mines_cnt = moves_done  = flags_marked = right_flags_marked = 0;
    char trash;
    bool game_over = false;

    while (SIZE_Y == 0 && SIZE_X == 0){
        std::cout << "Введите через пробел размер поля (x, y) и кол-во мин: [";
        std::cin >> SIZE_X >> SIZE_Y >> mines_cnt;
        std::cout << "размер поля по х: " << SIZE_X << endl;
        std::cout << "размер поля по у: " << SIZE_Y << endl;
        std::cout << "кол-во мин: " << mines_cnt << endl;
        clear_cin();
    }
    
    /*
    std::cout << "включить debug_mode? (если у вас ошибка, включите пж, жизнь мне в +100500 раз упростите...)"
    << " [y/n] (default - n): ";
    trash = tolower(cin.get());
    if (trash == 'y')
        debug_mode = true;
    else{
        if (trash != '\n')
            clear_cin();
        debug_mode = false;
    }
    */
    //global_map_init();
    vector_2d_init(player_map);
    print_screen();
    int start_x, start_y; start_x = start_y = SIZE_X;
    while (start_x < 0 || start_y < 0 || start_x >= SIZE_X || start_y >= SIZE_Y){
        print("Введите стартовые 'х' и 'у', в которых точно не будет бомбы")
        cin >> start_x >> start_y;
    }
    global_map_init(start_x, start_y);

    if (debug_mode)
        print_screen(true);
    // ИГРА THE GAME
    //right_flags_marked = mines_cnt;
    while (!game_over){
        if (right_flags_marked == mines_cnt){
            for (int _ = 0; _ < randint(0, static_cast<int>(congrats.size()/4)); ++_){
                std::cout << congrats[randint(0, congrats.size()-1)] << ' ';
            }std::cout << endl;
            print("Попробовать ещё раз? [y/n] (default - n)")
            trash = tolower(cin.get());

            for (int _ = 0; _ < 10; ++_)
                std::cout << endl;

            if (trash == 'y')
                goto new_game;
            else
                exit(0);
        }

        print_screen();
        game_now:
        print("Введите через пробел команду, х, у")
        print("отобразить список команд 'h'")

        int x, y;
        bool help_mode = false, skip = false;

        if (start_x != -1 && start_y != -1){
            x = start_x;
            y = start_y;
            start_x = start_y = -1;
            trash = 'e';
        }
        else{
            cin >> trash; trash = tolower(trash);
        
            if (trash == 'h')
                help_mode = true;
            if (trash == 's')
                skip = true;

            if (!help_mode && !skip){
                cin >> x >> y;
                --x; --y;
                if (x < 0 || x >= SIZE_X){
                    print("введён слишком большой x")
                    goto game_now;

                }
                if (y < 0 || y >= SIZE_Y){
                    print("введён слишком большой y")
                    goto game_now;
                }
            }
        }
        

        if (help_mode)
            trash = 'q';
        switch (trash)
        {
        case 'q':
            if (help_mode){
                print("q - ставит флаг '!' (здесь должна быть бомба)")
            }
            else{
                if (player_map[y][x] == HERE_SHOULD_BE_BOMB){
                    player_map[y][x] = CLOSED_CELL;
                    --flags_marked;
                    if (global_map[y][x] == HERE_BOMB){
                        if (debug_mode)
                            print("Здесь бомба, но вы убрали флаг")
                        --right_flags_marked;
                    }

                }
                else{
                    player_map[y][x] = HERE_SHOULD_BE_BOMB;
                    ++flags_marked;
                    if (global_map[y][x] == HERE_BOMB){
                        if (debug_mode)
                            print("Здесь бомба, правильный флаг")
                        ++right_flags_marked;
                    }
                }
                break;
            }

        case 'w':
            if (help_mode){
                print("w - ставит '?' (может здесь бомба?)")
            }
            else{
                if (player_map[y][x] == HERE_SHOULD_BE_BOMB)
                    --flags_marked;

                player_map[y][x] = MAYBE_HERE_BOMB;
                break;
            }

        case 'e':
            if (help_mode){
                print("e - очищает клетку (если в клетке была бомба - game over)")
            }
            else{
                vector_2d checked_cells;
                vector_2d_init(checked_cells);
                open_cell(x, y, checked_cells);
                break;
            }
        
        case 's':
            if (help_mode){
                print("s - единоразово показывает всё поле, с цифрами и бомбами (читы)")
            }
            else{
                print_screen(true);
                break;
            }
        default:
            std::cout << "unknown command: пошёл нахуй [" << trash << endl;
            break;
        }
        ++moves_done;
    }
}

void print_screen(bool show_all){
    // меню сверху:
    std::cout << "|  Всего бомб: " << mines_cnt << "  |  Ходов сделано: " << moves_done
    << "  |  Флагов поставлено: " << flags_marked
    << "  |" << endl;
    for (int _; _ < 5; ++_)
        std::cout << ' ';
    std::cout << endl;

    // основное поле:
    for (int y = SIZE_Y-1; y >= 0; --y){
        std::cout << y+1 << " :";
        for (int x = 0; x < SIZE_X; ++x){

            if (show_all){
                if (global_map[y][x] == HERE_BOMB)
                    std::cout << '*';
                else
                    std::cout << global_map[y][x];
            }
            else{
                switch (player_map[y][x])
                {
                case CLOSED_CELL:
                    std::cout << '#';
                    break;
                case OPENED_CELL:
                    std::cout << '0';
                    break;
                case HERE_SHOULD_BE_BOMB:
                    std::cout << '&';
                    break;
                case MAYBE_HERE_BOMB:
                    std::cout << '?';
                    break;
                default:
                    if (100 < player_map[y][x] && player_map[y][x] < 110){
                        std::cout << player_map[y][x] - 100;
                    }
                    else{
                        std::cout << endl << endl << endl << " ----!!! ОШИБКА !!!----"
                        << "неизвестный символ в player_map" << endl
                        << " y: " << y << " x: " << x << " а именно [" << player_map[y][x] << ']';
                        exit(-1);
                    }
                    break;
                }
            }

        } std::cout << endl;
    }
}

void open_cell(int x, int y, vector_2d & checked_cells){
    if (checked_cells[y][x] == OPENED_CELL)
        return;
    
    checked_cells[y][x] = OPENED_CELL;
    player_map[y][x] = OPENED_CELL;

    for (int mod_y = -1; mod_y < 2; ++mod_y){
        if (0 > y + mod_y || y + mod_y >= SIZE_Y)
            continue;

        for (int mod_x = -1; mod_x < 2; ++mod_x){
            if (0 > x + mod_x || x + mod_x >= SIZE_X || checked_cells[y + mod_y][x + mod_x] == OPENED_CELL)
                continue;

            if (global_map[y + mod_y][x + mod_x] == 0){ // ноль бомб вокруг
                player_map[y + mod_y][x + mod_x] = OPENED_CELL;
                open_cell(x + mod_x, y + mod_y, checked_cells);
            }
            else if (global_map[y + mod_y][x + mod_x] == HERE_BOMB)
                {
                    std::cout << "here bomb: x: " << x + mod_x << " y: " << y + mod_y << endl;
                    print_screen(true);
                    return;
                }
            else
                player_map[y + mod_y][x + mod_x] = 100 + global_map[y + mod_y][x + mod_x];
        }
    }
}

void vector_2d_init(vector_2d & some_vec){
    std::vector<int> empty_x (SIZE_X, CLOSED_CELL);
    for (int _ = 0; _ < SIZE_Y; ++_)
        some_vec.push_back(empty_x);
}

void global_map_init(int empty_x, int empty_y){
    if (debug_mode)
        print("создаём поле...")
    if (empty_x == -1 || empty_y == -1){
        if (debug_mode)
            print("стартовые х || у (-1), так что выберем рандомно..")
        empty_x = randint(0, SIZE_X);
        empty_y = randint(0, SIZE_Y);
    }
    vector_2d_init(global_map);

    if (debug_mode)
        print("теперь расставляем случайно мины...")

    int mines_left = mines_cnt;
    while (mines_left){
        int y = randint(0, SIZE_Y-1);
        int x = randint(0, SIZE_X-1);
        
        if (global_map[y][x] != HERE_BOMB && y != empty_y && x != empty_x){
            --mines_left;
            global_map[y][x] = HERE_BOMB;
            if (debug_mode)
                std::cout << "mine in x:" << x << " | y:" << y << endl;

            for (int mod_y = -1; mod_y < 2; ++mod_y){
                if (0 > y + mod_y || y + mod_y >= SIZE_Y)
                    continue;
                for (int mod_x = -1; mod_x < 2; ++mod_x){
                    if (0 > x + mod_x || x + mod_x >= SIZE_X)
                        continue;
                    
                    if (global_map[y + mod_y][x + mod_x] != HERE_BOMB){
                        ++global_map[y + mod_y][x + mod_x];
                    }
                }
            }
        }

    }

}

int randint(int start_num, int end_num){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> rand_gen(start_num, end_num);

    return rand_gen(gen);
}

void clear_cin(){
    //print("start cleaning")
    cin.clear();
    while (cin.get() != '\n');
    //print("end of clearing")
}

