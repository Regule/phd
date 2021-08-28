extern crate gym;
extern crate rand;

use gym::{GymClient};
use log::{self, info, Record, Level, Metadata, LevelFilter};


static GLOBAL_LOGGER: SimpleLogger = SimpleLogger{};


fn main() {
    log::set_logger(&GLOBAL_LOGGER).expect("Failed to initialize logger.");
    log::set_max_level(LevelFilter::Info);
	let client = GymClient::default();
	let _env = client.make("BipedalWalker-v3");
    info!("Loaded bipedal walker environment.");
}


struct SimpleLogger;

impl log::Log for SimpleLogger {
    fn enabled(&self, metadata: &Metadata) -> bool {
        metadata.level() <= Level::Info
    }

    fn log(&self, record: &Record) {
        if self.enabled(record.metadata()) {
            println!("{} - {}", record.level(), record.args());
        }
    }

    fn flush(&self) {}
}
