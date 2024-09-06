#include <iostream>
#include <vector>
#include <random>
#include <stdexcept>

using std::cout;
using std::endl;
using std::cin;
using game_map = std::vector<std::vector<int>>;
using inputs_map = std::vector<std::vector<char>>;
#define print(x) cout << x << endl;

enum {NO_BALL, HERE_BALL, MAYBE_HERE_BALL};
enum {INPUT_UP, INPUT_RIGHT, INPUT_DOWN, INPUT_LEFT};

const char INPUT_NOT_USED = '-';
const char INPUT_COME_BACK = '^';
const char INPUT_HIT = '!';

const bool debug_mode = true;


int count_digit(int num);
void shoot_lazer(game_map &lazers_field, const game_map &used_field, inputs_map &, char direction, int num, bool check=true);
void field_init(game_map &game_field, int SIZE_Y, int SIZE_X, int balls_cnt);
void clear_cin();
void cout_spaces(int cnt);
void print_field(const game_map &player_field, const game_map &lazers_field, const inputs_map &);

//TODO: совсем мелочь: осталось дописать остатки случаев лазера (когда они срабатывают в самом начале)
int main(){
    start_game:
    print("enter count of balls:")
    print("easy peasy - 4, easy - 6, normal - 8")
    int balls_cnt =4; 
    cin >> balls_cnt; cin.get();
    int SIZE_X = 5;
    int SIZE_Y = 5;

    // настоящее поле, на котором спрятаны мячи
    game_map game_field(SIZE_Y, std::vector<int>(SIZE_X, static_cast<int>(NO_BALL)));  
    field_init(game_field, SIZE_Y, SIZE_X, balls_cnt);
    // поле, которое отображается на экране, можно ставить обозначения и флажки
    game_map player_field(SIZE_Y, std::vector<int>(SIZE_X, static_cast<int>(NO_BALL))); 
    // поле с лазерами, отображать поверх player_field
    game_map lazers_field(SIZE_Y, std::vector<int>(SIZE_X, static_cast<int>(NO_BALL)));
    game_map lazers_field_cleaned_copy = lazers_field;

    std::vector<std::vector<char>> inputs_used(4);
    inputs_used[INPUT_UP] = std::vector<char>(SIZE_X, INPUT_NOT_USED);
    inputs_used[INPUT_RIGHT] = std::vector<char>(SIZE_Y, INPUT_NOT_USED);
    inputs_used[INPUT_DOWN] = std::vector<char>(SIZE_X, INPUT_NOT_USED);
    inputs_used[INPUT_LEFT] = std::vector<char>(SIZE_Y, INPUT_NOT_USED);
    if (debug_mode)
        print_field(game_field, lazers_field, inputs_used);


    while (true){  // Собственно, игра:
        print_field(player_field, lazers_field, inputs_used);
        print("? {X} {Y} [возможно здесь шар] | 0 {X} {Y} [здесь шар]")
        print("e {w/a/s/d} {num} [пустить лазер] | f {w/a/s/d} {num} [предугадать лазер]")
        print("c [очистить лазеры] | h [подробное объяснение] | p [вы закончили]")

        switch (cin.get())
        {   
            int x, y;
            char command;
        case '?':
            cin >> x >> y;
            player_field[y-1][x-1] = MAYBE_HERE_BALL;
            break;
        case '0':
            cin >> x >> y;
            player_field[y-1][x-1] = HERE_BALL;
            break;
        case 'e':
            cin >> command;
            cin >> x;
            shoot_lazer(lazers_field, game_field, inputs_used, command, x-1, false);
            lazers_field = lazers_field_cleaned_copy;
            break;
        case 'f':
            cin >> command;
            cin >> x;
            shoot_lazer(lazers_field, player_field, inputs_used, command, x-1);
            break;
        case 'c':
            lazers_field = lazers_field_cleaned_copy;
            break;
        case 'h':
            print("Вы ввели 'h', начинаем поверхностный гайд:")
            print("Перед вами игра в чёрный ящик, объяснить правила? y/n [default n]")
            print("Вы ввели 'n', объясняем команды:")
            cout << endl;
            print("? {X} {Y}")
            print("? означает, что вы предполагаете, возможно здесь шар")
            print("{} фигурные скобки писать ненужно")
            cout << endl;
            print("0 {X} {Y}")
            print("0 означает, что вы уверены, здесь шар")
            cout << endl;
            print("e {w/a/s/d} {num}")
            print("после 'e' введите один из этих символов {w/a/s/d}, чтобы выбрать расположение входа лазера")
            print("дальше вводите число (например: e a 3) пустить лазер из координат 1 3")
            print("эта команда пускает лазер в коробку, НЕ учитывая ваши шары")
            break;
        case 'p':
            print_field(game_field, lazers_field, inputs_used);
            print("this is the end, you want to try again? y/n [default n]")
            cin >> command;
            if (command == 'y')
                goto start_game;
            else
                exit(1);
            break;
        default:
            print("Недопустимый ввод, попробуйте ещё раз.")
            break;
        }
        clear_cin();
    }
}


int count_digit(int num){
    if (num < 1)
        throw std::runtime_error("Был подсчитан разряд числа меньше '1'");
    int digit_cnt = 1;
    while (true){
        if (num / pow(10, digit_cnt) >= 1)
            ++digit_cnt;
        else
            return digit_cnt;
    }
}

int lazers_out_cnt = 0;
void shoot_lazer(game_map &lazers_field, const game_map &used_field, inputs_map &inputs_used, char input, int num, bool check){
    enum {DIRECT_UP, DIRECT_RIGHT, DIRECT_DOWN, DIRECT_LEFT};
    int direction, x, y;
    const int SIZE_X = used_field[0].size();
    const int SIZE_Y = used_field.size();
    switch (input)
            {
            case 'w':
                direction = DIRECT_DOWN;
                input = INPUT_UP;
                x = num;
                y = 0;
                break;
            case 'd':
                direction = DIRECT_LEFT;
                input = INPUT_RIGHT;
                x = SIZE_X - 1;
                y = num;
                break;
            case 's':
                direction = DIRECT_UP;
                input = INPUT_DOWN;
                x = num;
                y = SIZE_Y - 1;
                break;
            case 'a':
                direction = DIRECT_RIGHT;
                input = INPUT_LEFT;
                x = 0;
                y = num;
                break;
            default:
                print("Введено неверное направление, теперь всё заново")
                return;
                break;
            }
    bool first_call = (inputs_used[input][num] == INPUT_NOT_USED ? (true) : (false));

    int balls_around;
    while ((-1 < y && y < SIZE_Y) && (-1 < x && x < SIZE_X)){
        if (debug_mode)
            cout << "lazer now: " << x << ' ' << y << endl;
        lazers_field[y][x] = 1;
        balls_around = 0;

        if (debug_mode){
            for (int y = SIZE_Y-1; y > -1; --y){
                for (int x = 0; x < SIZE_X; ++x){
                    if (lazers_field[y][x])
                        cout << '+';
                    else
                        cout << '#';
                }cout << endl;
            }
        }
        
        int here_mod_y, here_mod_x;
        for (int mod_y = -1; mod_y < 2; ++mod_y){
            if (-1 >= y + mod_y || y + mod_y >= SIZE_Y)
                    continue;
            for (int mod_x = -1; mod_x < 2; ++mod_x){
                if (-1 >= x + mod_x || x + mod_x >= SIZE_X)
                    continue;

                if (used_field[y + mod_y][x + mod_x] != NO_BALL){
                    ++balls_around;
                    // проверка на попадание
                    if ((direction == DIRECT_UP && mod_y == 1 && mod_x == 0) || 
                    (direction == DIRECT_RIGHT && mod_y == 0 && mod_x == 1) ||
                    (direction == DIRECT_DOWN && mod_y == -1 && mod_x == 0) ||
                    (direction == DIRECT_LEFT && mod_y == 0 && mod_x == -1)){
                        if (debug_mode)
                            print("HIT IN BALL")
                        if (!check)
                            inputs_used[input][num] = INPUT_HIT;
                        return;
                    }
                    // проверка на возвращение
                    else if (balls_around >= 2){
                        if (debug_mode)
                            print("COME BACK!!!")
                        if (!check)
                            inputs_used[input][num] = INPUT_COME_BACK;
                        return;
                    }
                    else{
                        here_mod_x = mod_x;
                        here_mod_y = mod_y;
                    }
                }

            }
        }
        if (debug_mode)
            print("reflection")
        if (here_mod_x == 1 && here_mod_y == 1){
            if (direction == DIRECT_RIGHT){
                direction = DIRECT_DOWN; }
            else if (direction == DIRECT_UP){
                direction = DIRECT_LEFT; }
        }

        else if (here_mod_x == 1 && here_mod_y == -1){
            if (direction == DIRECT_RIGHT){
                direction = DIRECT_UP;}
            else if (direction == DIRECT_DOWN){
                direction = DIRECT_LEFT;}
        }

        else if (here_mod_x == -1 && here_mod_y == -1){
            if (direction == DIRECT_LEFT){
                direction = DIRECT_UP;}
            else if (direction == DIRECT_DOWN){
                direction = DIRECT_RIGHT;}
        }

        else if (here_mod_x == -1 && here_mod_y == 1){
            if (direction == DIRECT_LEFT){
                direction = DIRECT_DOWN;}
            else if (direction == DIRECT_UP){
                direction = DIRECT_RIGHT;}
        }
        else{
            print("somehow dont reflect any")
        }

        switch (direction)
                {
                case DIRECT_UP:
                    ++y;
                    break;
                case DIRECT_RIGHT:
                    ++x;
                    break;
                case DIRECT_DOWN:
                    --y;
                    break;
                case DIRECT_LEFT:
                    --x;
                    break;
                default:
                    throw std::runtime_error("shoot_lazer странное направление! (direction)");
                    break;
                }
    }

    // Если дошёл до сюда, значит лазер вышел из коробки не в изначальную позицию
    char symbol = static_cast<char>('A' + lazers_out_cnt);
    inputs_used[input][num] = symbol;
    switch (direction)
    {
    case DIRECT_UP:
        inputs_used[INPUT_UP][x] = symbol;
        break;
    case DIRECT_RIGHT:
        inputs_used[INPUT_RIGHT][y] = symbol;
        break;
    case DIRECT_DOWN:
        inputs_used[INPUT_DOWN][x] = symbol;
        break;
    case DIRECT_LEFT:
        inputs_used[INPUT_LEFT][y] = symbol;
        break;
    default:
        throw std::runtime_error("shoot_lazer() somehow miss DIRECT at the end of func");
        break;
    }
    ++lazers_out_cnt;
}


void field_init(game_map &field, int SIZE_Y, int SIZE_X, int balls_cnt){
    //fill_2d_vector(field, SIZE_Y, SIZE_X, static_cast<int>(NO_BALL));

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist_y(0, SIZE_Y-1);
    std::uniform_int_distribution<> dist_x(0, SIZE_X-1);

    while (balls_cnt){
        int y = dist_y(gen);
        int x = dist_x(gen);
        
        if (field[y][x] == NO_BALL){
            --balls_cnt;
            field[y][x] = static_cast<int>(HERE_BALL);
            if (debug_mode)
                cout << "ball in x:" << x << " | y:" << y << endl;
        }

    }return;
}


void clear_cin(){
    if (debug_mode)
        print("start cleaning")
    cin.clear();
    char a = cin.get();
    while(a != '\n'){
        cout << a;
        a = cin.get();
    }
    if (debug_mode)
        print("end of clear")
}


void cout_spaces(int cnt){
    for (int _ = 0; _ < cnt; ++_)
        cout << ' ';
}


void print_field(const game_map &player_field, const game_map &lazers_field, const inputs_map &inputs_used){
    const int SIZE_Y = player_field.size();
    const int SIZE_X = player_field[0].size();
    
    int indent_y = count_digit(SIZE_Y) + 1;
    int indent_x = count_digit(SIZE_X);
    
    // UI Сверху
    print("- не просмотренно, ^ вернулся, ! попал\n")

    // индексы сверху
    cout_spaces(indent_y + 1);
    for (int num = 1; num <= SIZE_X; ++num){  
        cout << num;
        cout_spaces(indent_x - count_digit(num));
    }cout << endl;

    // состояние входов для лазеров
    cout_spaces(indent_y + 1);
    for (int x = 0; x < SIZE_X; ++x){  
        cout << inputs_used[INPUT_UP][x];
        cout_spaces(indent_x - 1);
    }cout << endl;


    // Отрисовка поля
    for (int y = SIZE_Y - 1; y > -1; --y){
        // UI Слева
        cout << y+1 << ' ' << inputs_used[INPUT_LEFT][y];

        for (int x = 0; x < SIZE_X; ++x){
            if (lazers_field[y][x])
                cout << '+';
            else
                switch (player_field[y][x])
                {
                case NO_BALL:
                    cout << '#';
                    break;
                case HERE_BALL:
                    cout << '0';
                    break;
                case MAYBE_HERE_BALL:
                    cout << '?';
                    break;
                default:
                    break;
                }
        }
        // UI Справа
        cout << inputs_used[INPUT_RIGHT][y] << endl;
    }


    // UI Снизу
    cout_spaces(indent_y + 1);
    for (int x = 0; x < SIZE_X; ++x){  
        cout << inputs_used[INPUT_DOWN][x];
        cout_spaces(indent_x - 1);
    }cout << endl;
}

