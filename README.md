# Orbiteer

A tool to control time-range based scripts

# Goals

1. Provide a consistent, elegant way of running a script repeatedly with varied inputs in a useful way, such as fitting a goal run-time.
2. Provide clear error handling and notification, failing gracefully.
3. Be highly configurable.
4. Be highly tested.


# Wanted Features

#### Legend:

| Symbol | Meaning |
|--------|---------|
| :white_check_mark: | Merged |
| :yellow_square: | In progress |
| :red_square: | Not yet begun |

### Iteration:
- :yellow_square: Iterate over datetime range
  - :yellow_square: Old -> New
  - :yellow_square: New -> Old
- :red_square: Iterate over item chunks
  - :red_square: In presented order
  - :red_square: Sorted

### Target Measurement
- :yellow_square: Direct time taken by command
- :yellow_square: Number returned by command

### Optimization Strategy
- :yellow_square: Direct ratio
  - :yellow_square: With damping
- :red_square: PID

### Targets
- :yellow_square: Run command line
  - :yellow_square: Args at end of command string
  - :red_square: Command line formatting
- :red_square: Call URL
  - :red_square: Via request parameters
  - :red_square: Via request body
- :red_square: Append to file

### Failure retries
- :yellow_square: Quit
- :red_square: N retries (before quit)
  - :red_square: Immediately
  - :red_square: Timed wait
  - :red_square: Exponential backoff
- :red_square: Skip
  - :red_square: Retry pattern and then skip
  - :red_square: Skip and retry again at end of run

### Notification methods
- :yellow_square: Logs
- :red_square: User-named scripts
- :red_square: [PushOver](https://pushover.net/)

### Notification events
- :yellow_square: Nominal completion
- :yellow_square: Erroring out
- :red_square: N% completion
- :red_square: Time passed
