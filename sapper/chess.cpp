#include <iostream>
#include <fstream>
#include <vector>
#include <stdexcept>
#include <cctype>


using std::cout; 
using std::cin; 
using std::endl;
using std::string;

#define print(x) cout << x << endl;
constexpr char figur_prefix[3] = {"♟"[0], "♟"[1], '\0'};


bool can_move_here(char figurine, string team, int x1, int y1, int x2=-1, int y2=-1);
void print_screen(const string (&white_field)[8], const string (&black_field)[8], 
int cur_x=-1, int cur_y=-1);

std::vector<std::vector<bool>> possible_moves (8, std::vector<bool> (8));
std::vector<std::vector<bool>> clear_copy_possible_moves (8, std::vector<bool> (8));
int main(){
    string team_white_field[8]{};
    string team_black_field[8]{};
    
    team_black_field[7] = "♖♘♗♕♔♗♘♖";
    team_black_field[6] = "♙♙♙♙♙♙♙♙";
    
    team_white_field[1] = "♟♟♟♟♟♟♟♟";
    team_white_field[0] = "♜♞♝♛♚♝♞♜";

    string empty = "";
    for (int _ = 0; _ < 8*3; ++_){
        empty.push_back(' ');
    }

    team_black_field[5] = team_black_field[4] = team_black_field[3] 
    = team_black_field[2] = team_black_field[1] = team_black_field[0]
    = team_white_field[2] = team_white_field[3] = team_white_field[4]
    = team_white_field[5] = team_white_field[6] = team_white_field[7]
    = empty;


start_new_game:
    string team_turn_now = "white";
    string (*team_field_now)[8];
    string readline;
    int x1, y1, x2, y2;
    int curx = -1, cury = -1;
    while (true){
        print_screen(team_white_field, team_black_field, curx, cury);
        possible_moves = clear_copy_possible_moves;
        if (team_turn_now == "white"){
            print("Ход белых")
            team_field_now = &team_white_field;
        }
        else{
            print("Ход чёрных")
            team_field_now = &team_black_field;
        }
        
        while (true){
            getline(cin, readline);
            if (readline.size() <= 1){
                print("Введите хоть что-то (пропустить ход нельзя, увы)")
            }
            else
                break;
        }
        x1 = toupper(readline[0]) - 'A';
        y1 = readline[1] - '1';
        if (readline.size() == 2){
            if ((*team_field_now)[y1][x1] != ' '){
                print(can_move_here((*team_field_now)[y1][x1*3+2], team_turn_now, x1, y1))
                curx = x1;
                cury = y1;
            }
            else{
                print("У вас нет фигур в этом месте")
                // Чтобы снова ходить в следующем ходу (в конце флипнится)
                team_turn_now = (team_turn_now == "white" ? "black": "white");
            }
        }
        else{
            curx = cury = -1;
        }

        team_turn_now = (team_turn_now == "white" ? "black": "white");
    }
}


// в figurine передавать последний символ из трёх 
bool can_move_here(char figurine, string team, int x1, int y1, int x2, int y2){
    std::vector<std::vector<bool>> moves (8, std::vector<bool> (8));

    #define move(coordinate, add) (team == "white" ? coordinate + add : coordinate - add)

    switch (figurine)
    {
        case "♟"[2]: case "♙"[2]:
            moves[move(y1, 1)][x1] = 1;
            moves[move(y1, 2)][x1] = 1;
            break;
        case "♛"[2]: case "♕"[2]:

        case "♚"[2]: case "♔"[2]:
            break;
        case "♝"[2]: case "♗"[2]:
            break;
        case "♞"[2]: case "♘"[2]:
            moves[move(y1, 2)][x1-1] = 1;
            moves[move(y1, 2)][x1+1] = 1;
            moves[move(y1, -2)][x1-1] = 1;
            moves[move(y1, -2)][x1+1] = 1;

            moves[move(y1, 1)][x1-2] = 1;
            moves[move(y1, 1)][x1+2] = 1;
            moves[move(y1, -1)][x1-2] = 1;
            moves[move(y1, -1)][x1+2] = 1;
            break;
        case "♜"[2]: case "♖"[2]:
            break;
        default:
            print("___ERROR!!!::")
            cout << team << ' ' << x1 << ' ' << y1 << " to " 
            << x2 << ' ' << y2 << endl;
            break;
    }
    
    if (x2 == y2 && y2 == -1){
        possible_moves = moves;
        return true;
    }

    return (moves[y2][x2]);
}


void print_screen(const string (&white_field)[8], const string (&black_field)[8], 
int cur_x, int cur_y){
    char edge_line[] = "  +---+---+---+---+---+---+---+---+";

    for (int y = 7; y > -1; --y){
        print(edge_line)
        cout << y+1 << ' ';

        for (int cx = 0; cx < 8; ++cx){
            int x = cx * 3;
            cout << '|';
            
            // Если сейчас выбрали для хода эту фигуру
            if (cur_x != cx || cur_y != y)
                cout << ' ';

            if (white_field[y][x] != ' '){
                if (cur_x == cx && cur_y == y)  // Если выбрали эту фигуру
                    cout << '*';
                cout << figur_prefix << white_field[y][x+2];
                if (possible_moves[y][cx] == true)  // Если можно срубить эту фигуру
                    cout << '*';

            }
            else if (black_field[y][x] != ' '){
                if (cur_x == cx && cur_y == y)  // Если выбрали эту фигуру
                    cout << '*';
                cout << figur_prefix << black_field[y][x+2];
                if (possible_moves[y][cx] == true)  // Если можно срубить эту фигуру
                    cout << '*';
            }
            else if (possible_moves[y][cx] != false) // Сюда можно сходить
                cout << '*';
            else
                cout << ' ';
            
            cout << ' ';
        }cout << '|' << endl;
    }print(edge_line)

    char coords[] = "ABCDEFGH";
    cout << "  ";
    for (int i = 0; i < 8; ++i){
        cout << "  " << coords[i] << ' ';
    }cout << endl;
}

