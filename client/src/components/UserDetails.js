import React, { useState, useCallback, useMemo } from 'react';
import { 
    Container, TextField, Button, Typography, Paper, 
    Divider, List, ListItem, ListItemText, Grid, Select, MenuItem 
} from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';


import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const UserDetails = () => {
    const [incomeDate, setIncomeDate] = useState('');
    const [incomeDetails, setIncomeDetails] = useState('');
    const [incomeAmount, setIncomeAmount] = useState('');
    const [expenseDate, setExpenseDate] = useState('');
    const [expenseDetails, setExpenseDetails] = useState('');
    const [expenseAmount, setExpenseAmount] = useState('');
    const [expenseCategory, setExpenseCategory] = useState('');
    const [investmentDate, setInvestmentDate] = useState('');
    const [investmentCategory, setInvestmentCategory] = useState('');
    const [investmentSymbol, setInvestmentSymbol] = useState('');
    const [investmentAmount, setInvestmentAmount] = useState('');
    const [investmentType, setInvestmentType] = useState('');
    const [userDetails, setUserDetails] = useState(null);


    const token = useMemo(() => localStorage.getItem('token'), []);

    const combinedData = useMemo(() => {
        if (!userDetails) return [];

        // Assuming each array has its own date property
        const allData = [
            ...userDetails.incomes.map(item => ({...item, type: 'income'})),
            ...userDetails.expenses.map(item => ({...item, type: 'expense'})),
            ...userDetails.investments.map(item => ({...item, type: 'investment'}))
        ];
    
        return allData.sort((a, b) => new Date(a.date) - new Date(b.date));
    }, [userDetails]);

    const dataMapping = useMemo(() => ({
        income: { 
            income_date: incomeDate || new Date().toISOString(), 
            income_details: incomeDetails || 'Added from frontend', 
            income_amount: parseFloat(incomeAmount) 
        },
        expense: { 
            expense_date: expenseDate || new Date().toISOString(), 
            expense_details: expenseDetails || 'Spent from frontend', 
            expense_amount: parseFloat(expenseAmount), 
            expense_category: expenseCategory || 'Others' 
        },
        investment: { 
            date_of_investment: investmentDate || new Date().toISOString(), 
            investment_category: investmentCategory || 'Example Category', 
            investment_symbol: investmentSymbol || 'SYM', 
            investment_amount: parseFloat(investmentAmount), 
            investment_type: investmentType || 'stock' 
        }
    }), [incomeDate, incomeDetails, incomeAmount, expenseDate, expenseDetails, expenseAmount, expenseCategory, investmentDate, investmentCategory, investmentSymbol, investmentAmount, investmentType]);


    const apiCall = useCallback(async (endpoint, method = 'GET', data = null) => {
        const headers = {
            'Authorization': `Bearer ${token}`
        };
        if (data) {
            headers['Content-Type'] = 'application/json';
        }
        const response = await fetch(`http://localhost:8000${endpoint}`, {
            method,
            headers,
            body: data ? JSON.stringify(data) : null
        });
        return await response.json();
    }, [token]);

    const fetchUserDetails = useCallback(async () => {
        try {
            const data = await apiCall('/user_details');
            setUserDetails(data);
        } catch (error) {
            console.error("Error fetching user details:", error);
        }
    }, [apiCall]);

    const handleSubmit = useCallback(async (type) => {
        const endpoint = `/add_${type}`;
        const data = dataMapping[type];
        try {
            await apiCall(endpoint, 'POST', data);
        } catch (error) {
            console.error("Error adding details:", error);
        }
    }, [apiCall, dataMapping]);

    return (
        <Container maxWidth="md">
            <Typography variant="h4" gutterBottom>User Details</Typography>

            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Typography variant="h6">Income</Typography>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DatePicker
                            label="Date"
                            value={incomeDate}
                            onChange={(newValue) => setIncomeDate(newValue)}
                            renderInput={(params) => <TextField {...params} fullWidth variant="outlined" />}
                        />
                    </LocalizationProvider>
                    <TextField fullWidth value={incomeDetails} onChange={e => setIncomeDetails(e.target.value)} label="Details" variant="outlined" />
                    <TextField fullWidth value={incomeAmount} onChange={e => setIncomeAmount(e.target.value)} label="Amount" variant="outlined" />
                    <Button variant="contained" color="primary" onClick={() => handleSubmit('income')}>Add Income</Button>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Typography variant="h6">Expense</Typography>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DatePicker
                            label="Date"
                            value={expenseDate}
                            onChange={(newValue) => setExpenseDate(newValue)}
                            renderInput={(params) => <TextField {...params} fullWidth variant="outlined" />}
                        />
                    </LocalizationProvider>
                    <TextField fullWidth value={expenseDetails} onChange={e => setExpenseDetails(e.target.value)} label="Details" variant="outlined" />
                    <TextField fullWidth value={expenseAmount} onChange={e => setExpenseAmount(e.target.value)} label="Amount" variant="outlined" />
                    <Select fullWidth value={expenseCategory} onChange={e => setExpenseCategory(e.target.value)} label="Category" variant="outlined">
                        <MenuItem value="Others">Others</MenuItem>
                        <MenuItem value="Food">Food</MenuItem>
                        <MenuItem value="Travel">Travel</MenuItem>
                    </Select>
                    <Button variant="contained" color="primary" onClick={() => handleSubmit('expense')}>Add Expense</Button>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Typography variant="h6">Investment</Typography>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DatePicker
                            label="Date of Investment"
                            value={investmentDate}
                            onChange={(newValue) => setInvestmentDate(newValue)}
                            renderInput={(params) => <TextField {...params} fullWidth variant="outlined" />}
                        />
                    </LocalizationProvider>
                    <TextField fullWidth value={investmentSymbol} onChange={e => setInvestmentSymbol(e.target.value)} label="Symbol" variant="outlined" />
                    <TextField fullWidth value={investmentAmount} onChange={e => setInvestmentAmount(e.target.value)} label="Amount" variant="outlined" />
                    <Select fullWidth value={investmentType} onChange={e => setInvestmentType(e.target.value)} label="Type" variant="outlined">
                        <MenuItem value="stock">Stock</MenuItem>
                        <MenuItem value="bond">Bond</MenuItem>
                    </Select>
                    <Button variant="contained" color="primary" onClick={() => handleSubmit('investment')}>Add Investment</Button>
                </Grid>
            </Grid>


            <Button variant="contained" color="secondary" onClick={fetchUserDetails} style={{ marginTop: 20 }}>
                Download Report
            </Button>

            {userDetails && userDetails.incomes && userDetails.expenses && userDetails.investments &&  (
                <Paper elevation={3} style={{ marginTop: 20, padding: 20 }}>
                    <Typography variant="h5" gutterBottom>Email: {userDetails.email}</Typography>

                    <Divider style={{ margin: '20px 0' }} />

                    {/* Assuming you want a LineChart for income, expense, and investment */}
                    <Typography variant="h6">Income, Expense, and Investment Over Time:</Typography>
            <LineChart width={600} height={300} data={combinedData}>
                <XAxis dataKey="date" />
                <YAxis />
                <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
                <Tooltip />
                <Line type="monotone" dataKey={data => data.type === 'income' ? data.income_amount : null} stroke="#8884d8" name="Income" />
                <Line type="monotone" dataKey={data => data.type === 'expense' ? data.expense_amount : null} stroke="#82ca9d" name="Expense" />
                <Line type="monotone" dataKey={data => data.type === 'investment' ? data.investment_amount : null} stroke="#ffc658" name="Investment" />
            </LineChart>

                    <Typography variant="h6">Incomes:</Typography>
                    <List>
                        {userDetails.incomes.map((income, index) => (
                            <ListItem key={index}>
                                <ListItemText 
                                    primary={`Amount: ${income.income_amount}`}
                                    secondary={`Details: ${income.income_details}, Date: ${income.income_date}`}
                                />
                            </ListItem>
                        ))}
                    </List>

                    <Typography variant="h6">Expenses:</Typography>
                    <List>
                        {userDetails.expenses.map((expense, index) => (
                            <ListItem key={index}>
                                <ListItemText 
                                    primary={`Amount: ${expense.expense_amount}`}
                                    secondary={`Details: ${expense.expense_details}, Date: ${expense.expense_date}, Category: ${expense.expense_category}`}
                                />
                            </ListItem>
                        ))}
                    </List>

                    <Typography variant="h6">Investments:</Typography>
                    <List>
                        {userDetails.investments.map((investment, index) => (
                            <ListItem key={index}>
                                <ListItemText 
                                    primary={`Amount: ${investment.investment_amount}`}
                                    secondary={`Category: ${investment.investment_category}, Symbol: ${investment.investment_symbol}, Type: ${investment.investment_type}, Date: ${investment.date_of_investment}`}
                                />
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}
        </Container>
    );
}

export default UserDetails;
