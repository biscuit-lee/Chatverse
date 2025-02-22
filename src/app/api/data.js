export default async function handler(req, res) {
    const response = await fetch('http://localhost:5000/api/data');
    const data = await response.json();
    res.status(200).json(data);
  }