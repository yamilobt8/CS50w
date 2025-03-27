document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}` )
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      const emailsView = document.getElementById("emails-view");

      emailsView.innerHTML = "";

      if (emails.length === 0) {
        if (mailbox == 'inbox') {
          emailsView.innerHTML = "<p>No emails In Inbox</p>";
        }else{
          emailsView.innerHTML = `<p>No emails ${mailbox}ed</p>`;
        }
        return; // Stop execution
      }

      emails.forEach(email => {
        const emailDiv = document.createElement("div");
        emailDiv.innerHTML = `
          <strong>From:</strong> ${email.sender} <br>
          <strong>To:</strong> ${email.recipients.join(", ")} <br>
          <strong>Subject:</strong> ${email.subject} <br>
          <strong>Timestamp:</strong> ${email.timestamp} <br>
          <hr>
        `;
        emailsView.appendChild(emailDiv);
      });
  })
  .catch(error => console.error("Error fetching emails:", error));
}

function send_email(event) {
  
  event.preventDefault();
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
}