struct AiGymMetadata{
	int cycle;
	float reward;
	int running;
	int error_code;
	string error_msg;
};

std::ostream & operator << (std::ostream &out, const AiGymMetadata &metadata);

class AiGymAPI{
private:
	string observation_pipe;
	string reaction_pipe;
	string metadata_pipe;
	int observation_size;
	int reaction_size;

public:
	AiGymAPI(const string& observation_pipe, const string& reaction_pipe,
		   	const string& metadata_pipe, int observation_size, int reaction_size);

	arma::Mat<double> get_observation() const;

	void send_reaction(const arma::Mat<double> &reaction) const;

	AiGymMetadata get_metadata() const;

};
