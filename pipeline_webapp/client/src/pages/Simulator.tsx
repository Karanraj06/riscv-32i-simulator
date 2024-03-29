import Stats from '../components/Stats';
import { useState } from 'react';
// import useFetch from "../hooks/useFetch";
import { useEffect } from 'react';
import { decToHex, binToHex, binToDec } from '../utilities/baseConversion';
import StatsBlock from '../components/StatsBlock';

export default function Simulator() {
  const [getId, setgetId] = useState(1);
  const [rg, setrg] = useState<Array<number>>(Array(32).fill(0));
  const [ci, setci] = useState<string[]>(['', '', '', '', '']);
  const [cf, setcf] = useState<string[]>(['', '', '']);
  const [cd, setcd] = useState<string[]>(['', '', '']);
  const [stats, setStats] = useState<Array<number>>(Array(12).fill(0));
  const [mem, setMem] = useState({});
  const [istats, setIstats] = useState<Array<any>>([
    4,
    4,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    ['', '', ''],
    ['', '', ''],
  ]);
  const [dstats, setDstats] = useState<Array<any>>([
    4,
    4,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    ['', '', ''],
    ['', '', ''],
  ]);
  const [activeTab, setActiveTab] = useState('CacheComp1');

  function handleTabChange(newtab: string) {
    setActiveTab(newtab);
  }

  // let { loading, error, value } = useFetch("http://127.0.0.1:8000/run", {}, [
  //     getId1,
  // ]);

  // ({ loading, error, value } = useFetch("http://127.0.0.1:8000/step", {}, [
  //     getId2,
  // ]));

  // ({ loading, error, value } = useFetch("http://127.0.0.1:8000/reset", {}, [
  //     getId3,
  // ]));

  // useEffect(() => {
  //     if (typeof error !== "undefined") alert("Error: " + error);
  // }, [getId1, getId2, getId3]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/data')
      .then(response => response.json())
      .then(data => {
        setci(data.current_instruction);
        setcd(data.dependencies);
        setcf(data.forwarding_paths);
        setrg(data.registers);
        setStats(data.stats);
        setMem(data.memory);
        setIstats(data.istats);
        setDstats(data.dstats);
        console.log(dstats[10]);
      });
  }, [getId]);

  function handleRun() {
    fetch('http://127.0.0.1:8000/run')
      .then(response => response.json())
      .then(data => {
        if (!data.success) {
          alert('Invalid Machine Code');
        } else {
          setgetId(getId + 1);
        }
      })
      .catch(error => {
        alert('Invalid Machine Code');
      });
  }

  function handleStep() {
    fetch('http://127.0.0.1:8000/step')
      .then(response => response.json())
      .then(data => {
        if (!data.success) {
          alert('Invalid Machine Code');
        } else {
          setgetId(getId + 1);
        }
      })
      .catch(error => {
        alert('Invalid Machine Code');
      });
  }

  function handleReset() {
    fetch('http://127.0.0.1:8000/reset')
      .then(response => response.json())
      .then(data => {
        if (!data.success) {
          alert('Invalid Machine Code');
        } else {
          setgetId(getId + 1);
        }
      })
      .catch(error => {
        alert('Invalid Machine Code');
      });
  }

  const regComponent = (
    <>
      <div className='my-10'>
        <Stats label='Clock Cycles' val={stats[0]} />
        <Stats label='Instruction Executed' val={stats[1]} />
        <Stats label='CPI' val={parseFloat(stats[2].toFixed(4))} />
        <Stats
          label='Data-transfer (load and store) instructions executed'
          val={stats[3]}
        />
        <Stats label='ALU instructions executed' val={stats[4]} />
        <Stats label='Control instructions executed' val={stats[5]} />
        <Stats label='Stalls' val={stats[6]} />
        <Stats label='Data Hazards' val={stats[7]} />
        <Stats label='Control Hazards' val={stats[8]} />
        <Stats label='Branch Mispredictions' val={stats[9]} />
        <Stats label='Stalls due to Data Hazards' val={stats[10]} />
        <Stats label='Stalls due to Control Hazards' val={stats[11]} />
      </div>

      <div className='grid md:grid-flow-col md:grid-cols-2 gap-20 items-start'>
        {/* Registers Start */}
        <div className='grid gap-2'>
          {/* Heading */}
          <h1 className='my-4 text-xl text-emerald-500 text-center'>
            Registers
          </h1>
          {/* Table Heading */}
          <div className='flex justify-evenly'>
            <p className='text-teal-500 hover:text-black'>Register</p>
            <p className='text-teal-500 hover:text-black'>Hex</p>
            <p className='text-teal-500 hover:text-black'>Decimal</p>
          </div>
          {/* x0 - x31 */}
          <div className='grid gap-4' id='registers'>
            {rg.map((r, i) => (
              <div className='flex justify-evenly font-mono' key={i}>
                <div>x{i}</div>
                <div className='border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400'>
                  {decToHex(r)}
                </div>
                <div className='border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400'>
                  {r}
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* Registers End */}
        {/* Memory Starts */}
        <div className='grid gap-2'>
          {/* Heading */}
          <h1 className='my-4 text-xl text-emerald-500 text-center'>Memory</h1>
          {/* Table Heading */}
          <div className='flex justify-evenly'>
            <p className='text-teal-500 hover:text-black'>Address</p>
            <p className='text-teal-500 hover:text-black'>Hex</p>
            <p className='text-teal-500 hover:text-black'>Decimal</p>
          </div>
          {/* Data Memory */}
          <div className='grid gap-4' id='memory'>
            {Object.entries(mem).map(([key, value], index) => (
              <div className='flex justify-evenly font-mono' key={index}>
                <div>{decToHex(Number.parseInt(key))}</div>
                <div className='border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400'>
                  {typeof value === 'string' && binToHex(value)}
                </div>
                <div className='border border-gray-200 hover:border-emerald-400 w-28 rounded-sm text-center text-gray-400'>
                  {typeof value === 'string' && binToDec(value)}
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* Memory Ends */}
      </div>
    </>
  );

  // const [isLoading, setIsLoading] = useState(false);

  // const handleClick = () => {
  //     setIsLoading(true);
  //     fetch("http://127.0.0.1:8000/file")
  //         .then(response => response.json())
  //         .then(data => {
  //             console.log(data);
  //             setIsLoading(false);
  //         })
  //         .catch(error => {
  //             console.error(error);
  //             setIsLoading(false);
  //         });
  // };

  const cacheComponent = (
    <>
      <div className='my-10'></div>

      <div className='grid md:grid-flow-col md:grid-cols-2 gap-20 items-start'>
        {/* Registers Start */}
        <div className='grid gap-2'>
          {/* Heading */}
          <h1 className='my-4 text-xl text-emerald-500 text-center'>
            Instruction Cache
          </h1>
          {/* Table Heading */}
          <div className='grid gap-4' id='registers'>
            <StatsBlock label='Block Size' value={istats[0]} />
            <StatsBlock label='Cache Size' value={istats[1]} />
            <StatsBlock label='# Sets' value={istats[2]} />
            <StatsBlock label='# Accessess' value={istats[3]} />
            <StatsBlock label='# Hits' value={istats[4]} />
            <StatsBlock label='# Misses' value={istats[5]} />
            <StatsBlock label='# Cold Misses' value={istats[6]} />
            <StatsBlock label='# Capacity Misses' value={istats[7]} />
            <StatsBlock label='# Conflict Misses' value={istats[8]} />
            <StatsBlock label='# Memory Stalls' value={istats[9]} />
            <StatsBlock
              label='# Prev Address Tag'
              value={istats[10][0]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Address Index'
              value={istats[10][1]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Address Block Offset'
              value={istats[10][2]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Victim Tag'
              value={istats[11][0]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Victim Index'
              value={istats[11][1]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Victim Block Offset'
              value={istats[11][2]}
              c='text-sm'
            />
          </div>
        </div>
        <div className='grid gap-2'>
          {/* Heading */}
          <h1 className='my-4 text-xl text-emerald-500 text-center'>
            Data Cache
          </h1>
          {/* Table Heading */}
          <div className='grid gap-4' id='registers'>
            <StatsBlock label='Block Size' value={dstats[0]} />
            <StatsBlock label='Cache Size' value={dstats[1]} />
            <StatsBlock label='# Sets' value={dstats[2]} />
            <StatsBlock label='# Accessess' value={dstats[3]} />
            <StatsBlock label='# Hits' value={dstats[4]} />
            <StatsBlock label='# Misses' value={dstats[5]} />
            <StatsBlock label='# Cold Misses' value={dstats[6]} />
            <StatsBlock label='# Capacity Misses' value={dstats[7]} />
            <StatsBlock label='# Conflict Misses' value={dstats[8]} />
            <StatsBlock label='# Memory Stalls' value={dstats[9]} />
            <StatsBlock
              label='# Prev Address Tag'
              value={dstats[10][0]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Address Index'
              value={dstats[10][1]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Address Block Offset'
              value={dstats[10][2]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Victim Tag'
              value={dstats[11][0]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Victim Index'
              value={dstats[11][1]}
              c='text-sm'
            />
            <StatsBlock
              label='# Prev Victim Block Offset'
              value={dstats[11][2]}
              c='text-sm'
            />
          </div>
        </div>
        {/* Memory Ends */}
      </div>
      {/* <div className="flex justify-center m-10">
                <button
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    onClick={handleClick}
                    disabled={isLoading}
                >
                    {isLoading ? "Loading..." : "Load File"}
                </button>
            </div> */}
    </>
  );

  return (
    <>
      <div className='grid p-4 gap-4 align-top auto-rows-[4em]'>
        <h1 className='my-4 text-xl text-emerald-500 text-center'>Simulator</h1>
        <div className='grid grid-flow-col grid-cols-[18%_40%_14%_14%] gap-2 justify-between'>
          <div></div>
          <div className='text-emerald-500 break-words'>
            Current Instruction
          </div>
          <div className='text-emerald-500 break-words'>Dependency</div>
          <div className='text-emerald-500 break-words'>Forwarding Path</div>
        </div>
        <div className='grid grid-flow-col grid-cols-[18%_40%_14%_14%] gap-2 justify-between'>
          <div className='flex items-center break-words'>Instruction Fetch</div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {ci[0]}
          </div>
          <div className='pl-1'></div>
          <div className='pl-1'></div>
        </div>
        <div className='grid grid-flow-col grid-cols-[18%_40%_14%_14%] gap-2 justify-between'>
          <div className='flex items-center break-words'>Decode</div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {ci[1]}
          </div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {cd[0]}
          </div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {cf[0]}
          </div>
        </div>
        <div className='grid grid-flow-col grid-cols-[18%_40%_14%_14%] gap-2 justify-between'>
          <div className='flex items-center break-words'>Execute</div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {ci[2]}
          </div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {cd[1]}
          </div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {cf[1]}
          </div>
        </div>
        <div className='grid grid-flow-col grid-cols-[18%_40%_14%_14%] gap-2 justify-between'>
          <div className='flex items-center break-words'>Memory Access</div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {ci[3]}
          </div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {cd[2]}
          </div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {cf[2]}
          </div>
        </div>
        <div className='grid grid-flow-col grid-cols-[18%_40%_14%_14%] gap-2 justify-between'>
          <div className='flex items-center break-words'>Write Back</div>
          <div className='border border-gray-200 text-gray-400 font-mono align-middle flex items-center overflow-auto pl-1 hover:border-emerald-400'>
            {ci[4]}
          </div>
          <div className='pl-1'></div>
          <div className='pl-1'></div>
        </div>
        <div className='flex flex-wrap justify-evenly items-end'>
          <button
            className='bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-md'
            onClick={handleRun}
          >
            Run
          </button>
          <button
            className='bg-yellow-400 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded-md'
            onClick={handleStep}
          >
            Step
          </button>
          <button
            className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md'
            onClick={handleReset}
          >
            Reset
          </button>
        </div>
      </div>

      <div className='my-10'>
        <nav className='flex justify-center gap-10'>
          <button
            className={`mr-2 ${
              activeTab === 'CacheComp1' ? 'bg-blue-500 text-white' : ''
            } px-4 rounded-sm`}
            onClick={() => handleTabChange('CacheComp1')}
          >
            Registers / Memory
          </button>
          <button
            className={`ml-2 ${
              activeTab === 'CacheComp2' ? 'bg-blue-500 text-white' : ''
            } px-4 rounded-sm`}
            onClick={() => handleTabChange('CacheComp2')}
          >
            Cache
          </button>
        </nav>
        {activeTab === 'CacheComp1' ? regComponent : cacheComponent}
      </div>
    </>
  );
}
