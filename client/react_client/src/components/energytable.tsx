import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import Table from "./table";
import Pagination from "./pagination";
import Dailydatachart from "./dailytable";

export interface EnergyData {
  date: string;
  total_production: number;
  total_consumption: number | null;
  avg_price: number;
  longest_negative_hours: number;
}


const EnergyDashboard: React.FC = () => {
  const [data, setData] = useState<EnergyData[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  const DataFormater = (number: number) => {
    // Formatter from
    // https://stackoverflow.com/questions/52320447/recharts-set-y-axis-value-base-of-number-displayed
    if(number > 1000000000){
      return (number/1000000000).toString() + 'B';
    }else if(number > 1000000){
      return (number/1000000).toString() + 'M';
    }else if(number > 1000){
      return (number/1000).toString() + 'K';
    }else{
      return number.toString();
    }
  }

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/daily-stats/?page=${page}&size=10`)
      .then((res) => res.json())
      .then((json) => {
        setData(json.data);
        setTotalPages(Math.ceil(json.total / json.size));
      });
  }, [page]);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Energy Data Dashboard</h1>
      <Table data={data} onDateSelect={setSelectedDate}/>
      <Pagination page={page} totalPages={totalPages} onPageChange={setPage} />
      <div className="mt-6">
        <h2 className="text-lg font-bold">Electricity Production and Consumption</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <XAxis dataKey="date" />
            <YAxis tickFormatter={DataFormater}/>
            <Tooltip />
            <Line type="monotone" dataKey="total_production" stroke="#8884d8" name="Production MWh/day" />
            <Line type="monotone" dataKey="total_consumption" stroke="#82ca9d" name="Consumption MWh/day" />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div>
      {selectedDate ? (
        <Dailydatachart selectedDate={selectedDate} />
      ) : (
        <p className="text-center mt-4">Select a date from the table to view hourly data.</p>
      )}
      </div>
    </div>
  );
};

export default EnergyDashboard;
