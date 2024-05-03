# SeeMore proj

Project with free and paid content

## Description

This project is a Django-based web application designed to manage user subscriptions and other functions, as well as to publish both paid and free content.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/your_project.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    - Create a `.env` file in the project root and specify the necessary environment variables:

        ```
        POSTGRES_DB=your_database_name
        POSTGRES_USER=your_database_user
        POSTGRES_PASSWORD=your_database_password
        CELERY_BROKER_URL=your_broker_url
        CELERY_RESULT_BACKEND=
        STRIPE_PUBLIC_KEY=your_stripe_public_key
        STRIPE_SECRET_KEY=your_stripe_secret_key
        STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_key
        CACHE_ENABLED=True/False
        CACHE_LOCATION=location_of_cache
        ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the server:

    ```bash
    python manage.py runserver
    ```

6. Run Celery for handling asynchronous tasks:

    ```bash
    celery -A config beat -l info -S django
    ```

### If using docker

1. Create docker  
   
   ```bash
   docker compose build
   ```

2. Up/run docker

   ```bash
   docker compose up
   ```

## Usage

1. Go to the application's main page: [http://localhost:8000/](http://localhost:8000/)
2. Register or log in if you already have an account. Phone number can only contain digits, +, and - characters.
3. Use the application's features such as profile management, subscription creation and cancellation.
4. Unregistered user can only see free content
5. A registered user sees free content, can become an author, and can subscribe that allows him to see paid content.
6. Also registered user can temporarily deactivate his account, that may be activated again or deleted after 21 days. 
7. The subscription can be deactivated ahead of schedule manually by the user.


## Subscription

Subscription is carried out using Stripe. Subscription verification occurs by receiving a response from the Stripe server using a Webhook.  
For using Stripe source you must go to hte stripe official website [https://stripe.com/](https://stripe.com/) and take a keys for correct working.  

Subscription has 3 parameters: short, long and ultra.  

Short - 1 month subscription, that coast 300 rub.  
Long - 6 month subscription, that coast 1200 rub.  
Ultra - 1 year subscription, that coast 2100 rub.

The program itself tracks the user's remaining subscription time.  
After the subscription period ends, it is automatically canceled.


## Testing

You can run tests to ensure the functionality of the application:

```bash
python manage.py test
```

## Built-in Commands

1. Database creation

      ```bash
      python3 manage.py create_db
      ```
   This command will create database, or refresh it.

2. Drop database

      ```bash
      python3 manage.py drop_db
      ```
   This command will delete your database.

3. Create superuser

     ```bash
     python3 manage.py csu 
     ```
   This command will create superuser

4. Delete reports

      ```bash 
      python3 manage.py delete_reports <content_id>
      ```
   This command will remove all complaints from content based on its id.  
   Example: python3 manage.py delete_reports 1  
   It will remove all reports from content with id 1.

5. Populate database

      ```bash
      python3 manage.py populate_db
      ```
   This command will fill your database by test data.

6. Creating users for testing  

      ```bash
      python3 manage.py cgu
      ```  
   cgm - Create Gamma User. Gamma user hase no subscription and he isn't author.  

      ```bash
      python3 manage.py cau
      ```  
   cau - Create Alpha User. Alpha is author ans he has got 1 free content but he hasn't got subscription.
      ```bash
      python3 manage.py cou
      ```  
   cou - Create Omega User. Omega user has ultra subscription but he isn't author.

      ```bash
      python3 manage.py cbu
      ```
   cbu - Create Brutal User. Brutal user is author with 1 free content and 1 pad content and he is subscribed.

## Stack

- python
- postgresql
- django
- docker
- stripe
- celery
- crispy_forms