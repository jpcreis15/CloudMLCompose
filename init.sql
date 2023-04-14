CREATE TABLE inferences (
  id SERIAL PRIMARY KEY,
  input_sample VARCHAR(2000) NOT NULL,
  prediction VARCHAR(2000) NOT NULL,
  inference_time TIMESTAMP
);