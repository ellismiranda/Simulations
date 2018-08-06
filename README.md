# Simulations
A collection of simulation scripts created for various purposes.



### Ad Server:
  
  ```python
  python ad_server_simluation.py [number of advertisers] [number of ads to auction]
  ```
  
  
  A simulation of an ad server in which multiple advertisers (Ad) vie for the same ad slot. Advertisers and ad slots and their attribute values are randomly generated within pre-defined ranges.



### Multi Armed Bandit:

  ```python
  python multi_armed_bandit_simulation.py [number of bandits] [number of epochs] [default epsilon]
  ```

  A simulation of the classic Multi-Armed Bandit problem using a mixture of Thompson Sampling and Epsilon-Greedy strategies. Bandits and their payout probability are randomly generated.



### Multi Armed Bandit Allocation:

  ```python
  python multi_armed_bandit_allocation_simulation.py [number of bandits] [number of serves] [default epsilon]
  ```

  *Important*: Will only run if `multi_armed_bandit_simulation.py` is in the same directory.

  A simulation of a classic Multi-Armed Bandit modified to mock-allocate serves for an ad server.  It uses a mixture of Thompson Sampling and Epsilon-Decreasing strategies. Bandits and their payout probability are randomly generated.
