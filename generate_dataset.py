"""Generate a small SYNTHETIC email dataset (emails.csv) so the project runs out of the box.
For real results, replace emails.csv with a real dataset that has columns: text,label
(label: 1 = Phishing, 0 = Safe)."""
import random, csv
random.seed(42)

brands = ["PayPal", "Amazon", "Netflix", "HDFC Bank", "SBI", "Microsoft", "Google", "Apple", "Flipkart", "Paytm"]
bad_domains = ["secure-login-verify.com", "account-update-now.net", "bit.ly/3xYz9", "tinyurl.com/verify-me",
               "192.168.45.12/login", "paypa1-support.xyz", "amaz0n-billing.top", "update-info.click"]
good_domains = ["company.com", "github.com", "university.edu", "docs.google.com", "linkedin.com", "meet.example.org"]

phish_open = ["Dear customer,", "Dear user,", "Attention!", "URGENT:", "Security alert:", "Hello,", "Notice:"]
phish_body = [
    "Your {b} account has been suspended due to unusual activity. Verify your password immediately at http://{d}",
    "We detected a login from a new device. Confirm your identity within 24 hours or your account will be closed: http://{d}",
    "You have won a prize! Click http://{d} to claim your reward now. Limited time offer!!!",
    "Your payment of $499 failed. Update your billing information here http://{d} to avoid service interruption.",
    "Final warning: your {b} card is blocked. Enter your PIN and OTP at http://{d} to unblock.",
    "Invoice attached. Please log in at http://{d} with your credentials to view the document.",
    "Congratulations, you are selected for a refund of Rs 8,500. Submit bank details at http://{d}",
    "Your mailbox is full. Click http://{d} to upgrade storage or you will lose messages.",
]
safe_open = ["Hi team,", "Hello,", "Hi,", "Dear colleague,", "Good morning,", "Hey,"]
safe_body = [
    "Please find the meeting notes from yesterday. The next sync is on Thursday at 11 AM.",
    "The project report is ready for review. You can access the shared folder at https://{g}/reports",
    "Reminder: the assignment submission deadline is Friday. Let me know if you have any questions.",
    "Thanks for your order from {b}. Your package will arrive in 3 to 5 business days. Track it in your account.",
    "Here is the agenda for the workshop. Join using the link https://{g}/join when it starts.",
    "Your monthly statement is now available. Log in through the official {b} app to view it.",
    "Can we reschedule our call to next week? I will send a calendar invite shortly.",
    "Great work on the presentation! Attaching the slides for everyone. Let's discuss on Monday.",
    "Your password was changed successfully. If this was you, no action is needed.",
    "Lunch is planned for 1 PM in the cafeteria. Reply if you want a vegetarian option.",
]

rows = []
for _ in range(600):
    b, d, g = random.choice(brands), random.choice(bad_domains), random.choice(good_domains)
    text = random.choice(phish_open) + " " + random.choice(phish_body).format(b=b, d=d, g=g)
    if random.random() < 0.25:                      # harder phishing: calm tone, no urgency
        text = "Hello, please review the updated policy for your " + b + " account at http://" + d
    rows.append((text, 1))
for _ in range(600):
    b, g = random.choice(brands), random.choice(good_domains)
    text = random.choice(safe_open) + " " + random.choice(safe_body).format(b=b, g=g, d="")
    if random.random() < 0.20:                      # harder safe: urgent tone, real link
        text = "URGENT: please review the contract at https://" + g + "/docs before the 5 PM deadline."
    rows.append((text, 0))

random.shuffle(rows)
with open("emails.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["text", "label"]); w.writerows(rows)
print(f"emails.csv created with {len(rows)} rows (600 phishing, 600 safe)")
