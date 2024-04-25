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

## Usage

1. Go to the application's main page: [http://localhost:8000/](http://localhost:8000/)
2. Register or log in if you already have an account.
3. Use the application's features such as profile management, subscription creation and cancellation.
4. Unregistered user can only see free content
5. A registered user sees free content, can become an author, and can sign up for a subscription that allows them to see paid content.
6. Also registered user can temporarily deactivate his account, that may be activated again or deleted after 21 days.

## Subscription

Subscription is carried out using Stripe. Subscription verification occurs by receiving a response from the Stripe server using a Webhook.  
For using Stripe source you must go to hte stripe official website [https://stripe.com/](https://stripe.com/) and take a keys for correct working.

## Testing

You can run tests to ensure the functionality of the application:

```bash
python manage.py test
```
