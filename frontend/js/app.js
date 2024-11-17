// Smooth Scroll for Navigation Links
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        window.scrollTo({
            top: targetSection.offsetTop - 50, // Adjust for sticky header
            behavior: 'smooth',
        });
    });
});

// Contact Form Submission
document.getElementById('contact-form').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Thank you for contacting us! We will get back to you shortly.');
    this.reset();
});

// Hero Section Animation
window.addEventListener('scroll', () => {
    const heroContent = document.querySelector('.hero-content');
    const scrollY = window.scrollY;
    heroContent.style.transform = `translateY(${scrollY * 0.5}px)`;
});

// Chatbot Toggle
const chatbotContainer = document.getElementById('chatbot-container');

function toggleChatbot() {
    if (chatbotContainer.style.display === 'block') {
        chatbotContainer.style.display = 'none';
    } else {
        chatbotContainer.style.display = 'block';
    }
}

// Attach chatbot toggle to the "Start Chat" button
document.querySelector('.cta-button').addEventListener('click', toggleChatbot);
