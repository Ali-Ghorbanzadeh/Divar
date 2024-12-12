const loginUser = async (email, password) => {
  const response = await fetch('/api/token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access', data.access_token);
    localStorage.setItem('refresh', data.refresh_token);
    console.log('Login successful');
  } else {
    console.log('Login failed');
  }
};

// استفاده از تابع loginUser
loginUser('user@example.com', 'your_password');
