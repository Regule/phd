extern crate gym;
extern crate rand;

use gym::{GymClient, Environment, State, Action, GymError, SpaceData};
use log::{self, info, warn, debug, Record, Level, Metadata, LevelFilter};
use ndarray::{Array1, Array2, array};

static GLOBAL_LOGGER: SimpleLogger = SimpleLogger{level: LevelFilter::Info};


fn main() {
    log::set_logger(&GLOBAL_LOGGER).expect("Failed to initialize logger.");
	let client = GymClient::default();
    let walker = Walker::new(&client);
    let dummy_array = Array2::zeros((4, 3));
    walker.reset();
    loop{
        walker.step(&dummy_array);
    }
}

//=================================================================================================
//                                            LOGGER
//=================================================================================================

struct SimpleLogger{
    level: LevelFilter,
}


impl SimpleLogger{

    fn new(level: LevelFilter)-> SimpleLogger{
        SimpleLogger{level}
    }

    fn set_level(&mut self, level: LevelFilter){
        self.level = level;
    }
}

impl log::Log for SimpleLogger {
    fn enabled(&self, metadata: &Metadata) -> bool {
        metadata.level() <= Level::Debug
    }

    fn log(&self, record: &Record) {
        if self.enabled(record.metadata()) {
            println!("{} - {}", record.level(), record.args());
        }
    }

    fn flush(&self) {}
}


//=================================================================================================
//                                 WALKER ENVIRONMENT WRAPPER 
//=================================================================================================

struct WalkerState{
    observation: Array1<f64>,
    enabled: bool,
}

struct Walker<'a>{
    walker_env: Environment<'a>,
}

impl Walker<'_>{

    pub fn new(client: &GymClient) -> Walker{
	    let walker_env = client.make("BipedalWalker-v3");
        info!("Loaded bipedal walker environment.");
        Walker{walker_env}
    }

    pub fn reset(&self){
        self.walker_env.reset();
    }

    pub fn random_step(&self)-> WalkerState{
        self.walker_env.render();
	    let action = self.walker_env.action_space().sample().get_box().unwrap();
        debug!("Action ==> {}",action);
        let response = self.walker_env.step(&Action::BOX(action));
        let state = match response{
            Ok(st)=> st,
            Err(err)=>{
                warn!("GymError -> {}", err.to_string());
                State{observation: SpaceData::DISCRETE(0),
                reward: 0.0,
                is_done: true}
            }
        };
        WalkerState{observation: state.observation.get_box().unwrap(), enabled: !state.is_done}
    }

    pub fn step(&self, action: &Array1<f64>)-> WalkerState{
        self.walker_env.render();
        debug!("Action ==> {}",action);
        let response = self.walker_env.step(&Action::BOX(action));
        let state = match response{
            Ok(st)=> st,
            Err(err)=>{
                warn!("GymError -> {}", err.to_string());
                State{observation: SpaceData::DISCRETE(0),
                reward: 0.0,
                is_done: true}
            }
        };
        WalkerState{observation: state.observation.get_box().unwrap(), enabled: !state.is_done}
    }
}


//=================================================================================================
//                                WALKER AGENT IMPLEMENTATION 
//=================================================================================================

struct WalkerAI{
    neural_layers: Vec<Array1<f64>>,
    score: f64,
}

impl WalkerAI{

    pub fn new(layer_sizes: Vec<usize>)-> WalkerAI{
        let neural_layers = Vec<Array1<f64>>::new();
        for layer_size in layer_sizes{
            neural_layers.push();
        }
    }

    pub fn process_input(_observation: &Array2<f32>)-> Array2<f32>{
        Array2::zeros((4, 3))
    }

}
