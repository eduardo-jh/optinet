# optinet
Layout and pipe size optimization of water distribution systems

# Installation

The code is available at https://github.com/eduardo-jh/optinet. You could
simply clone the project:

    $ git clone https://github.com/eduardo-jh/optinet.git

# Requirements

* pandas
* numpy
* deap
* epanet-module (from OpenWaterAnalytics)

## Install epanet-module

Clone the repository from: https://github.com/OpenWaterAnalytics/epanet-python

A directory called *epanet-python* is created, inside there is another one
called *epanet-module* and a file called **epamodule.py**, this is the only
file we need (we are NOT going to use the other files or directories).
Copy the **epamodule.py** file into the libraries directory: *optinet/lib*.
The full path after rename will be *optinet/lib/epamodule.py*.

**IMPORTANT**: the *lib* directory is not sync with GitHub so you may need to
create it manually.

You should also repeat the process for the LICENSE file, as it is one of the
conditions for the redistribution of the code from OpenWaterAnalytics.

If you want you could also try the examples they provide to use their code.

# License

Copyright (C) 2020-2021 Eduardo Jiménez Hernández

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
