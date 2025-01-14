// src/components/CryptoTable.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Table, TableHead, TableBody, TableRow, TableCell,
    Paper, TableContainer, TableSortLabel
} from '@mui/material';
import { Box } from '@mui/system';

function CryptoTable() {
    const [cryptos, setCryptos] = useState([]);
    const [sortConfig, setSortConfig] = useState({ key: 'cmc_rank', direction: 'asc' });

    useEffect(() => {
        fetchCryptos();
    }, []);

    const fetchCryptos = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/cryptos');
            setCryptos(response.data.cryptos || []);
        } catch (err) {
            console.error('Error fetching cryptos:', err);
        }
    };

    const handleSort = (key) => {
        // If the same column is clicked, toggle direction. Otherwise set direction = 'asc'
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    // Sorting logic
    let sortedCryptos = [...cryptos];
    sortedCryptos.sort((a, b) => {
        const quoteA = a.quote.USD;
        const quoteB = b.quote.USD;

        let valueA;
        let valueB;

        switch (sortConfig.key) {
            case 'price':
                valueA = quoteA.price;
                valueB = quoteB.price;
                break;
            case 'percent_change_24h':
                valueA = quoteA.percent_change_24h;
                valueB = quoteB.percent_change_24h;
                break;
            case 'volume_24h':
                valueA = quoteA.volume_24h;
                valueB = quoteB.volume_24h;
                break;
            case 'market_cap':
                valueA = quoteA.market_cap;
                valueB = quoteB.market_cap;
                break;
            case 'cmc_rank':
            default:
                valueA = a.cmc_rank;
                valueB = b.cmc_rank;
        }

        if (valueA < valueB) return sortConfig.direction === 'asc' ? -1 : 1;
        if (valueA > valueB) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
    });

    const formatBillions = (num) => {
        if (!num) return '—';
        if (num >= 1e9) {
            return (num / 1e9).toFixed(2) + ' B';
        } else if (num >= 1e6) {
            return (num / 1e6).toFixed(2) + ' M';
        }
        return num.toFixed(2);
    };

    return (
        <Box sx={{ p: 2 }}>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>
                                <TableSortLabel
                                    active={sortConfig.key === 'cmc_rank'}
                                    direction={sortConfig.key === 'cmc_rank' ? sortConfig.direction : 'asc'}
                                    onClick={() => handleSort('cmc_rank')}
                                >
                                    #
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>
                                <TableSortLabel
                                    active={sortConfig.key === 'price'}
                                    direction={sortConfig.key === 'price' ? sortConfig.direction : 'asc'}
                                    onClick={() => handleSort('price')}
                                >
                                    Price
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel
                                    active={sortConfig.key === 'percent_change_24h'}
                                    direction={sortConfig.key === 'percent_change_24h' ? sortConfig.direction : 'asc'}
                                    onClick={() => handleSort('percent_change_24h')}
                                >
                                    24h Change
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel
                                    active={sortConfig.key === 'volume_24h'}
                                    direction={sortConfig.key === 'volume_24h' ? sortConfig.direction : 'asc'}
                                    onClick={() => handleSort('volume_24h')}
                                >
                                    24h Volume
                                </TableSortLabel>
                            </TableCell>
                            <TableCell>
                                <TableSortLabel
                                    active={sortConfig.key === 'market_cap'}
                                    direction={sortConfig.key === 'market_cap' ? sortConfig.direction : 'asc'}
                                    onClick={() => handleSort('market_cap')}
                                >
                                    Market Cap
                                </TableSortLabel>
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sortedCryptos.map((coin) => {
                            const quote = coin.quote.USD;
                            const price = quote.price?.toFixed(2);
                            const volume = quote.volume_24h;
                            const mc = quote.market_cap;
                            const change24h = quote.percent_change_24h;
                            const isNegative = change24h < 0;

                            return (
                                <TableRow key={coin.id}>
                                    <TableCell>{coin.cmc_rank}</TableCell>
                                    <TableCell>{coin.name}</TableCell>
                                    <TableCell>${price}</TableCell>
                                    <TableCell sx={{ color: isNegative ? 'red' : 'green' }}>
                                        {change24h?.toFixed(2)}%
                                    </TableCell>
                                    <TableCell>${formatBillions(volume)}</TableCell>
                                    <TableCell>${formatBillions(mc)}</TableCell>
                                </TableRow>
                            );
                        })}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
}

export default CryptoTable;