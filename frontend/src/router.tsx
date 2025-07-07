import { createBrowserRouter } from 'react-router-dom'
import Homepage from './components/HomePage'
import { Layout } from './layout'
export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Homepage /> },
    ],
  },
])