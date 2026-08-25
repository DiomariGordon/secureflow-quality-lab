# Exercise 3 — Failed-Login Rate Limit

## Objective

Add a basic educational control that limits repeated failed logins by normalized email and time window.

## Threat model questions

Before coding, answer:

- What abuse are we reducing?
- Could an attacker lock out another user?
- Should the response reveal whether an email exists?
- Where should counters be stored?
- How is the counter reset?
- What audit evidence is needed?

## Minimum tests

- A small number of failed attempts remains allowed.
- The threshold returns a controlled denial.
- A successful login resets or updates the correct state according to the requirement.
- Email casing does not create separate counters.
- The response does not reveal whether the account exists.

## Caution

This is a learning implementation, not a production distributed rate limiter. Production designs may use gateways, identity providers, Redis, device signals, IP reputation, and abuse monitoring.
