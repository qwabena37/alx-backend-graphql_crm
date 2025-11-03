1. install Redis and dependencies.
   sudo apt update
    sudo apt install redis-server -y
   sudo systemctl enable redis-server
   sudo systemctl start redis-server
   sudo systemctl status redis-server



2. Steps to Run migrations (python manage.py migrate).
⚙️ Step 1: Activate your virtual environment

If you created one earlier, activate it so Django runs in the correct environment:

source venv/bin/activate


You should see (venv) at the start of your terminal prompt.

🏗️ Step 2: Navigate to your project directory

Move into the folder that contains your manage.py file (usually the Django project root):

cd path/to/your/project


For example:

cd ~/crm_project


You can confirm by listing files:

ls


You should see:

manage.py
crm/

📦 Step 3: Apply migrations

Run the following command:

python manage.py migrate


✅ This will:

Create your database (if it doesn’t exist)

Apply all default Django migrations (auth, admin, sessions, etc.)

Apply any migrations for your custom apps (like crm)

🧰 Step 4: (Optional) Make migrations for your custom models

If you’ve created or changed models, you must first generate migration files:

python manage.py makemigrations


Then apply them:

python manage.py migrate

3. Steps to start Celery worker (celery -A crm worker -l info).
⚙️ Step 1: Make sure Redis is running

Celery uses Redis as the message broker, so confirm Redis is active.

Check Redis status:
redis-cli ping


You should see:

PONG


If not, start it:

Linux:

sudo systemctl start redis-server


macOS (Homebrew):

brew services start redis


Docker:

docker run -d --name redis -p 6379:6379 redis

🧩 Step 2: Activate your virtual environment

If you created one earlier:

source venv/bin/activate

📂 Step 3: Navigate to your project directory

Go to the folder that contains your manage.py file and the crm package:

cd path/to/your/project


Example:

cd ~/crm_project


You should see something like:

manage.py
crm/

🚀 Step 4: Start the Celery worker

Run this command:

celery -A crm worker -l info


Explanation:

-A crm → Tells Celery to use the app defined in crm/celery.py

worker → Starts the Celery worker process

-l info → Sets the logging level to “info” (you can also use debug for more details)

If everything is configured correctly, you’ll see output like:

[tasks]
  . crm.tasks.generate_crm_report

[INFO/MainProcess] Connected to redis://localhost:6379/0
[INFO/MainProcess] celery@yourhostname ready.


That means your Celery worker is listening for tasks.

🕒 Step 5: (Optional) Run Celery Beat

If you’ve set up scheduled tasks (like the weekly CRM report), you also need Celery Beat running in a separate terminal:

celery -A crm beat -l info


Beat handles the scheduling, while the worker actually performs the tasks.

✅ Step 6: Test the setup

You can manually trigger the Celery task to confirm it works:

python manage.py shell


Then run inside the shell:

from crm.tasks import generate_crm_report
generate_crm_report.delay()


If successful, you’ll see logs in your worker terminal and a report line in /tmp/crm_report_log.txt.

4. Steps to start Celery Beat (celery -A crm beat -l info).
⚙️ Step 1: Make sure prerequisites are ready
✅ Redis running

Celery Beat needs the same broker as Celery (Redis).
Check Redis is up:

redis-cli ping


If you see PONG, it’s running.

If not, start it:

Linux (Ubuntu/Debian):

sudo systemctl start redis-server


macOS (Homebrew):

brew services start redis


Docker:

docker run -d --name redis -p 6379:6379 redis

🧩 Step 2: Activate your virtual environment

If you’re using one (recommended):

source venv/bin/activate


You should see (venv) at the start of your terminal prompt.

📂 Step 3: Navigate to your Django project directory

Go to the folder where your manage.py file and crm app live:

cd path/to/your/project


Example:

cd ~/crm_project


You should see:

manage.py
crm/

🕒 Step 4: Start Celery Beat

Run the following command:

celery -A crm beat -l info


Explanation:

-A crm → Points to your Celery app defined in crm/celery.py.

beat → Starts the Celery Beat scheduler.

-l info → Shows info-level logs (you can use -l debug for more detailed output).

🧭 Step 5: Verify it’s working

When it starts, you should see logs like:

[INFO/MainProcess] beat: Starting...
[INFO/MainProcess] Scheduler: Sending due task generate-crm-report (crm.tasks.generate_crm_report)


That means Celery Beat is scheduling your weekly report task.

🧵 Step 6: Run Celery Worker (in another terminal)

Celery Beat only schedules tasks — it doesn’t execute them.
You must have a Celery worker running separately to process the scheduled jobs.

In a new terminal (with the same environment activated):

celery -A crm worker -l info


Now:

Beat sends the task on schedule

Worker executes it

✅ Step 7: (Optional) Test your schedule manually

You can force-run your task to confirm everything’s connected:

python manage.py shell


Then inside the Django shell:

from crm.tasks import generate_crm_report
generate_crm_report.delay()


You should see output in:

The Celery worker terminal (Task succeeded)

/tmp/crm_report_log.txt (your log file)


5. Steps to Verify logs in /tmp/crm_report_log.txt.
🧩 Step 1: Ensure the task has run

Make sure your Celery setup is working and the task has executed — either:

✅ Option 1: Let Celery Beat schedule it

If your CELERY_BEAT_SCHEDULE runs weekly (e.g., every Monday 6 AM), wait for the scheduled time, or temporarily change it to run every minute for testing:

'schedule': crontab(minute='*/1'),


Then restart Celery Beat and Worker:

celery -A crm beat -l info
celery -A crm worker -l info

✅ Option 2: Trigger manually

Run your task manually from the Django shell:

python manage.py shell


Then inside the shell:

from crm.tasks import generate_crm_report
generate_crm_report.delay()

📁 Step 2: Check if the log file exists

Run:

ls /tmp/crm_report_log.txt


If the file exists, you’ll see:

/tmp/crm_report_log.txt


If it doesn’t exist yet, the task may not have executed successfully — check your Celery worker logs for errors.

📝 Step 3: View the log contents

Use one of these commands:

🔹 View the full file:
cat /tmp/crm_report_log.txt

🔹 View only the last few entries:
tail /tmp/crm_report_log.txt

🔹 Watch the log in real time (for debugging):
tail -f /tmp/crm_report_log.txt


You should see lines similar to:

2025-11-03 06:00:00 - Report: 120 customers, 45 orders, 15000 revenue

🧠 Step 4: Troubleshooting if log is empty

If the file is missing or empty:

Check Celery Worker logs — see if the task ran successfully:

celery -A crm worker -l info


You should see something like:

Task crm.tasks.generate_crm_report succeeded


Ensure the file path is correct — the task writes to:

/tmp/crm_report_log.txt


If you’re on Windows or a non-standard environment, change it in your task to a path like:

BASE_DIR = Path(__file__).resolve().parent.parent
log_path = BASE_DIR / "crm_report_log.txt"


Check for permission issues:

touch /tmp/test.txt


If you get a “Permission denied,” run your services with a user that can write to /tmp.

✅ Step 5: Confirm new entries appear

After rerunning the task (manually or via schedule), check again:

tail /tmp/crm_report_log.txt


You should see a new line with the latest timestamp and updated data.