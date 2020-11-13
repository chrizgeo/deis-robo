-module(service).
-export([start/0, handle/0]).

start() -> spawn(service, handle, []).

handle() -> 
  receive Num -> io:format("Received a message with ~p.\n", [Num]), handle() end.
