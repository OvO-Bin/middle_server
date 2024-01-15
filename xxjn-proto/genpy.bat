for %%i in (*.proto) do protoc.exe -I=. --python_out=..\game\proto\  %%i
pause
