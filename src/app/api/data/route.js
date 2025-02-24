export async function GET() {
    try {
      const response = await fetch('http://localhost:5000/api/tweets');
      const data = await response.json();
      
      return Response.json(data)
    } catch (error) {
      //console.error('API error:', error);
      return Response.json(
        {error: 'FAILED'},
        {status: 500}
      )
    }
  }