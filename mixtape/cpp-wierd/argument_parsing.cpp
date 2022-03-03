#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string> 
#include<iostream>

using std::string;
using std::endl;
using std::cout;
using std::cerr;

class Config{
public:
	string in_pipe;
	string out_pipe;
	int observation_size;
	int reaction_size;
	int hidden_size;
	double mutation_rate;
	double mutation_factor;

	Config(){
		this->in_pipe = "/tmp/simulation_to_ai";
		this->out_pipe = "/tmp/ai_to_simulation";
		this->observation_size = 10;
		this->reaction_size = 3;
		this->hidden_size = 20;
		this->mutation_rate = 0.2;
		this->mutation_factor = 0.4;
	}

	bool parse_args(int argc, char **argv){
		int argument_char;
		while ((argument_char = getopt (argc, argv, "i:o:b:r:d:m:f:")) != -1){
			switch(argument_char){
				case 'i':
					this->in_pipe = string(optarg);
					break;
				case 'o':
					this->out_pipe = string(optarg);
					break;
				case 'b':
					this->observation_size = atoi(optarg);
					break;
				case 'r':
					this->reaction_size = atoi(optarg);
					break;
				case 'd':
					this->hidden_size = atoi(optarg);
					break;
				case 'm':
					this->mutation_rate = atof(optarg);
					break;
				case 'f':
					this->mutation_factor = atof(optarg);
					break;
				case 'h':
					print_help();
					return false;
				default:
					cerr << "Unknown argument - " << static_cast<char>(argument_char) << endl;
					return false;
			}
		}
		return true;
	}

	void print_config() const{
		for(int i=0; i<100; i++){
			cout<<'-';
		}
		cout<<endl;
		cout<<"CONFIGURATION :"<<endl;
		cout<<"In pipe = "<<this->in_pipe<<endl;
		cout<<"Out pipe = "<<this->out_pipe<<endl;
		cout<<"Observation size = "<<this->observation_size<<endl;
		cout<<"Reaction size = "<<this->reaction_size<<endl;
		cout<<"Hidden size = "<<this->hidden_size<<endl;
		cout<<"Mutation rate = "<<this->mutation_rate<<endl;
		cout<<"Mutation factor = "<<this->mutation_factor<<endl;
		for(int i=0; i<100; i++){
			cout<<'-';
		}
		cout << endl;	
	}

	void print_help(){
		cout << "This program executes neuroevolution algorithm and is prepared to work";
		cout << " with specific Open Ai gym wrapper" << endl;
	}
	
};

int  main (int argc, char **argv){
	Config cfg;
	if(cfg.parse_args(argc, argv)){
		cfg.print_config();	
	}
}

int  tutorial_main (int argc, char **argv){
  int aflag = 0;
  int bflag = 0;
  char *cvalue = NULL;
  int index;
  int c;

  opterr = 0;


  while ((c = getopt (argc, argv, "abc:")) != -1)
    switch (c)
      {
      case 'a':
        aflag = 1;
        break;
      case 'b':
        bflag = 1;
        break;
      case 'c':
        cvalue = optarg;
        break;
      case '?':
        if (optopt == 'c')
          fprintf (stderr, "Option -%c requires an argument.\n", optopt);
        else if (isprint (optopt))
          fprintf (stderr, "Unknown option `-%c'.\n", optopt);
        else
          fprintf (stderr,
                   "Unknown option character `\\x%x'.\n",
                   optopt);
        return 1;
      default:
        abort ();
      }


  printf ("aflag = %d, bflag = %d, cvalue = %s\n",
          aflag, bflag, cvalue);

  for (index = optind; index < argc; index++)
    printf ("Non-option argument %s\n", argv[index]);
  return 0;
}

