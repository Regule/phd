#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// To debug: fprintf(stderr, "Debug messages...\n");
#define WHITE 'W'
#define BLACK 'B'
#define EMPTY '.' 
#define BLOCKED '#'
#define UNINITIALIZED -1

typedef struct Move_s{
    int x;
    int y;
    bool pass;
} Move;

typedef struct Player_s{
    Move move;
    Move last;
    int score;
    char color;
} Player;

typedef struct Board_s{
  int size;
  char *fields;  
} Board;

Player me;
Player opponent;
Board board;
bool border_filled = false;

void read_config(){
    char my_color[2];
    scanf("%[^\n]", my_color);
    me.color = my_color[0];
    if(me.color==WHITE){
        opponent.color=BLACK;
    }else{
        opponent.color=WHITE;
    }
    scanf("%d", &(board.size));
    board.fields = (char*)malloc(board.size*board.size*sizeof(char));
    opponent.last.x = UNINITIALIZED;
    opponent.last.y = UNINITIALIZED;
    me.last.x = UNINITIALIZED;
    me.last.y = UNINITIALIZED;
}

char board_get_field(int x, int y){
    //fprintf(stderr,"CHEVKING %d %d\n", x, y);
    if(x<0||x>=board.size||y<0||y>=board.size) return BLOCKED;
    return board.fields[y*board.size+x];
}

char board_get_field_for_move(const Move *move){
    return board_get_field(move->x, move->y);
}

bool is_valid_move(const Move *old, const Move *new){
    //if(old->pass||old->x!=new->x||old->y!=new->y){
        return board_get_field_for_move(new)==EMPTY;
    //}
    //return false;
}

void read_turn(){
        scanf("%d%d", &opponent.last.x, &opponent.last.y);
        scanf("%d%d", &me.score, &opponent.score); 
        fgetc(stdin);
        for (int i = 0; i < board.size; i++) {
            // A row of the current board where 'B' marks a black stone, 'W' marks a white stone and '.' marks an empty field
            char line[board.size + 1];
            scanf("%[^\n]", line);
            fgetc(stdin);
            memcpy(board.fields+i*board.size, line, board.size);
        }

}

void board_print(){
    for (int y = 0; y < board.size; y++) {
        fprintf(stderr,"%*.*s\n", board.size, board.size,board.fields+y*board.size);
    }
}

void random_move(){
    me.move.x = rand() % board.size;
    me.move.y = rand() % board.size;
    me.move.pass = !is_valid_move(&me.last, &me.move);
}

bool dumb_surround(){
    static Move last;
    Move dumb;
    if(!last.pass){
        for(int dx=-1; dx<=1;dx++){
            for(int dy=-1; dy<=1;dy++){
                if(dx!=0&&dy!=0)continue;
                dumb.x = last.x+dx;
                dumb.y = last.y+dy;
                if(is_valid_move(&me.last, &dumb)){
                    dumb.pass=false;
                    me.move=dumb;
                    return true;   
                }
            }
        }
        last.pass=true;
    }
    for(int x=0; x<board.size; x++){
        for(int y=0; y<board.size; y++){
            if(board_get_field(x,y)==opponent.color){
                for(int dx=-1; dx<=1;dx++){
                    for(int dy=-1; dy<=1;dy++){
                        if(dx!=0&&dy!=0)continue;
                        dumb.x = x+dx;
                        dumb.y = y+dy;
                        if(is_valid_move(&me.last, &dumb)){
                            dumb.pass=false;
                            me.move=dumb;
                            last = dumb;
                            return true;   
                        }
                    }
                }
            }
        }
    }
    last.pass=true;
    return false;
}

bool fill_border(){
    Move border;
    border.x=0;
    while(1){
        for(int y=0;y<board.size;y++){
            border.y=y;
            if(is_valid_move(&me.last, &border)){
                border.pass=false;
                me.move=border;
                return true;
            }
        }
        if(border.x==board.size-1) break;
        if(border.x==0) border.x=board.size-1;
    }
    border.y=0;
    while(1){
        for(int x=0;x<board.size;x++){
            border.x=x;
            if(is_valid_move(&me.last, &border)){
                border.pass=false;
                me.move=border;
                return true;
            }
        }
        if(border.y==board.size-1) break;
        if(border.y==0) border.y=board.size-1;
    }
    return false;
}

void make_decision(){
    if(dumb_surround()){
        fprintf(stderr,"DUMB SURROUND\n");
        return;
    }
    if(fill_border()){
        fprintf(stderr,"BORDER FILL\n");
        return;
    }
    fprintf(stderr,"RANDOM MOVE\n");
    random_move();
}

void make_move(){
    if(me.move.pass){
        printf("PASS\n");
    }else{
        printf("%d %d\n",me.move.x, me.move.y);
    }
    me.last = me.move;
}

int main(){
    time_t t;
    srand((unsigned) time(&t));
    read_config();
    while (1){
        read_turn();
        //board_print();
        make_decision();
        make_move();
    }

    return 0;
}
