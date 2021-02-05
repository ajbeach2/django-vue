async function getMe() {
  try {
    const response = await axios.get('/me');
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}

async function login() {
  try {
    const response = await axios.get('/me');
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}

async function logout() {
  try {
    const response = await axios.get('/me');
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}