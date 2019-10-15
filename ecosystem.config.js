module.exports = {

  apps : [{
      name: "worker",
      cwd: ".",
      script: "/projects/timetable_v2/venv/bin/python3",
      args: "-m celery -A cel worker -l info",
      watch: false,
      interpreter: "",
      max_memory_restart: "1G"
   },
   {
      name: "bot",
      cwd: ".",
      script: "/projects/timetable_v2/venv/bin/python3",
      args: "-m bot.py",
      watch: false,
      interpreter: "",
      max_memory_restart: "1G"
   }

  ]
	
};
