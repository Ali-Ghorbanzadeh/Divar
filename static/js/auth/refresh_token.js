const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh')

  const response = await fetch('/api/token/refresh/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      refresh: refreshToken,
    }),
  })

  if (response.ok) {
    const data = await response.json()
    localStorage.setItem('access', data.access_token)
    console.log('Token refreshed successfully')
  } else {
    console.log('Failed to refresh token')
  }
}

refreshToken()
