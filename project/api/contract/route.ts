import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // For demo purposes, return mock responses
    // In production, you'd connect to your Python backend or deploy it separately
    
    if (request.url.includes('/analyze')) {
      return NextResponse.json({
        success: true,
        analysis: {
          risk_score: 0.3,
          clauses: [
            {
              type: "Governing Law",
              content: "This agreement shall be governed by the laws of [State]",
              risk_level: "low"
            }
          ],
          recommendations: [
            "Consider adding more specific termination clauses",
            "Review liability limitations"
          ]
        }
      });
    }
    
    if (request.url.includes('/create')) {
      return NextResponse.json({
        success: true,
        contract: {
          title: "Service Agreement",
          content: "Generated contract content based on your requirements...",
          sections: ["Terms", "Payment", "Termination"]
        }
      });
    }
    
    return NextResponse.json({ error: 'Endpoint not found' }, { status: 404 });
    
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
