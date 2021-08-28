extern crate gym;
extern crate rand;

use gym::{Action, GymClient, State};
use rand::Rng;
use log::{self, info, error};

fn main() {
    log::set_max_level(log::LevelFilter::Debug);
	let client = GymClient::default();
	let env = client.make("BipedalWalker-v3");
    print!("Loaded bipedal walker environment.");
}
