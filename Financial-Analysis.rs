use std::f64::EPSILON;
                   
/// Function to calculate Net Present Value (NPV)
fn npv(discount_rate: f64, cash_flows: &[f64]) -> f64 {
    cash_flows.iter()
        .enumerate()
        .map(|(t, &cf)| cf / (1.0 + discount_rate).powi(t as i32 + 1))
        .sum()
}

/// Function to calculate Internal Rate of Return (IRR) using Newton-Raphson method
fn irr(cash_flows: &[f64], max_iter: usize, tol: f64) -> Option<f64> {
    let mut rate = 0.1;  // Initial guess
    for _ in 0..max_iter {
        let mut npv = 0.0;
        let mut d_npv = 0.0;
        
        for (t, &cf) in cash_flows.iter().enumerate() {
            let denominator = (1.0 + rate).powi(t as i32);
            npv += cf / denominator;
            d_npv -= (t as f64 * cf) / (denominator * (1.0 + rate));
        }

        if npv.abs() < tol {
            return Some(rate);
        }

        let new_rate = rate - npv / d_npv;
        if (new_rate - rate).abs() < EPSILON {
            return Some(new_rate);
        }
        rate = new_rate;
    }
    None
}

/// Function to calculate Compound Annual Growth Rate (CAGR)
fn cagr(initial_value: f64, final_value: f64, years: f64) -> f64 {
    (final_value / initial_value).powf(1.0 / years) - 1.0
}

/// Function to calculate Simple Moving Average (SMA)
fn simple_moving_average(prices: &[f64], period: usize) -> Vec<f64> {
    prices.windows(period)
        .map(|window| window.iter().sum::<f64>() / period as f64)
        .collect()
}

fn main() {
    // Example data
    let cash_flows = [-1000.0, 200.0, 300.0, 400.0, 500.0]; // Initial investment and yearly returns
    let discount_rate = 0.1; // 10% discount rate

    // NPV Calculation
    let npv_value = npv(discount_rate, &cash_flows);
    println!("Net Present Value (NPV): {:.2}", npv_value);

    // IRR Calculation
    match irr(&cash_flows, 100, 1e-6) {
        Some(irr_value) => println!("Internal Rate of Return (IRR): {:.2}%", irr_value * 100.0),
        None => println!("IRR calculation did not converge"),
    }

    // CAGR Calculation
    let cagr_value = cagr(1000.0, 2000.0, 5.0);
    println!("Compound Annual Growth Rate (CAGR): {:.2}%", cagr_value * 100.0);

    // SMA Calculation
    let stock_prices = [100.0, 102.0, 105.0, 110.0, 115.0, 120.0, 125.0];
    let sma_values = simple_moving_average(&stock_prices, 3);
    println!("Simple Moving Average (SMA) (3-period): {:?}", sma_values);
}
