/*
Sortable table 
Got help from this video and from chatgpt
https://youtu.be/EaxC_kOG03E?feature=shared
*/

import { MouseEventHandler, useCallback, useState } from "react";


type ElectricityData = {
  date: string;
  total_production: number;
  total_consumption: number | null;
  avg_price: number;
  longest_negative_hours: number;
}[];

type SortKeys = keyof ElectricityData[0];

type SortOrder = "ascn" | "desc";

// Sorting function
function sortData({
  tableData,
  sortKey,
  reverse,
}: {
  tableData: ElectricityData;
  sortKey: SortKeys;
  reverse: boolean;
}) {
  if (!sortKey) return tableData;

  const sortedData = [...tableData].sort((a, b) => {
    const valueA = a[sortKey] ?? 0;
    const valueB = b[sortKey] ?? 0;

    if (typeof valueA === "number" && typeof valueB === "number") {
      return valueA - valueB;
    } else if (typeof valueA === "string" && typeof valueB === "string") {
      return valueA.localeCompare(valueB);
    }

    return 0;
  });

  return reverse ? sortedData.reverse() : sortedData;
}

// Sorting button component
function SortButton({
  sortOrder,
  columnKey,
  sortKey,
  onClick,
}: {
  sortOrder: SortOrder;
  columnKey: SortKeys;
  sortKey: SortKeys;
  onClick: MouseEventHandler<HTMLButtonElement>;
}) {
  return (
    <button
      onClick={onClick}
      className="ml-1 text-gray-600"
    >
      {sortKey === columnKey ? (sortOrder === "desc" ? "↓" : "↑") : "↕"}
    </button>
  );
}

// Sortable table component
function SortableTable({ data, onDateSelect  }: { data: ElectricityData, onDateSelect: any  }) {
  const [sortKey, setSortKey] = useState<SortKeys>("date");
  const [sortOrder, setSortOrder] = useState<SortOrder>("ascn");

  const headers: { key: SortKeys; label: string }[] = [
    { key: "date", label: "Date" },
    { key: "total_production", label: "Total Production (MWh/day)" },
    { key: "total_consumption", label: "Total Consumption (MWh/day)" },
    { key: "avg_price", label: "Average Price (€/MWh)" },
    { key: "longest_negative_hours", label: "Longest consecutive time when electricity price has been negative in hours" },
  ];

  const sortedData = useCallback(
    () => sortData({ tableData: data, sortKey, reverse: sortOrder === "desc" }),
    [data, sortKey, sortOrder]
  );

  function changeSort(key: SortKeys) {
    setSortOrder(sortOrder === "ascn" ? "desc" : "ascn");
    setSortKey(key);
  }


  return (
    <div className="w-full">
      {/* Table */}
      <table className="w-full border-collapse border border-gray-300">
        <thead className="bg-gray-100">
          <tr>
            {headers.map((header) => (
              <th
                key={header.key}
                className="border p-2 cursor-pointer"
                onClick={() => changeSort(header.key)}
              >
                {header.label}
                <SortButton
                  columnKey={header.key}
                  onClick={() => changeSort(header.key)}
                  sortOrder={sortOrder}
                  sortKey={sortKey}
                />
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {sortedData().map((item) => (
            <tr key={item.date} className="text-center border">
              {/* Clickable Date */}
              <td className="border p-2 text-blue-500 underline cursor-pointer" onClick={() => onDateSelect(item.date)}>
                {item.date}
              </td>
              <td className="border p-2">{item.total_production !== null ? item.total_production.toFixed(2) : "N/A"}</td>
              <td className="border p-2">{item.total_consumption !== null ? item.total_consumption.toFixed(2) : "N/A"}</td>
              <td className="border p-2">{item.avg_price !== null ? item.avg_price.toFixed(2) : "N/A"}</td>
              <td className="border p-2">{item.longest_negative_hours}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SortableTable;
