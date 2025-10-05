import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'

interface ChartData {
  name: string
  count: number
  percentage: number
}

interface AnalyticsChartsProps {
  frameworks: ChartData[]
  aiModels: ChartData[]
  vectorDBs: ChartData[]
  infrastructure: ChartData[]
}

const COLORS = ['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#06B6D4', '#84CC16', '#F97316']

export const TechnologyBarChart = ({ data, title }: { data: ChartData[], title: string }) => (
  <div className="glass-card p-6">
    <h3 className="text-lg font-semibold text-dark-900 dark:text-white mb-6">{title}</h3>
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data.slice(0, 8)}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis 
          dataKey="name" 
          stroke="#9CA3AF"
          fontSize={12}
          angle={-45}
          textAnchor="end"
          height={80}
        />
        <YAxis stroke="#9CA3AF" fontSize={12} />
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#1F2937', 
            border: '1px solid #374151',
            borderRadius: '8px',
            color: '#F9FAFB'
          }}
        />
        <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  </div>
)

export const TechnologyPieChart = ({ data, title }: { data: ChartData[], title: string }) => (
  <div className="glass-card p-6">
    <h3 className="text-lg font-semibold text-dark-900 dark:text-white mb-6">{title}</h3>
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data.slice(0, 6)}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percentage }) => `${name} ${percentage}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="count"
        >
          {data.slice(0, 6).map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip 
          contentStyle={{ 
            backgroundColor: '#1F2937', 
            border: '1px solid #374151',
            borderRadius: '8px',
            color: '#F9FAFB'
          }}
        />
      </PieChart>
    </ResponsiveContainer>
  </div>
)

export const TrendLineChart = ({ data, title }: { data: ChartData[], title: string }) => {
  const trendData = data.slice(0, 8).map((item) => ({
    name: item.name,
    adoption: item.percentage,
    projects: item.count
  }))

  return (
    <div className="glass-card p-6">
      <h3 className="text-lg font-semibold text-dark-900 dark:text-white mb-6">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={trendData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="name" 
            stroke="#9CA3AF"
            fontSize={12}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis stroke="#9CA3AF" fontSize={12} />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#1F2937', 
              border: '1px solid #374151',
              borderRadius: '8px',
              color: '#F9FAFB'
            }}
          />
          <Line 
            type="monotone" 
            dataKey="adoption" 
            stroke="#3B82F6" 
            strokeWidth={2}
            dot={{ fill: '#3B82F6', strokeWidth: 2, r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export const AnalyticsCharts = ({ frameworks, aiModels, vectorDBs, infrastructure }: AnalyticsChartsProps) => {
  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <TechnologyBarChart data={frameworks} title="Popular Frameworks" />
        <TechnologyPieChart data={aiModels} title="AI Models Distribution" />
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <TrendLineChart data={vectorDBs} title="Vector Database Adoption" />
        <TechnologyBarChart data={infrastructure} title="Infrastructure Usage" />
      </div>
    </div>
  )
}
