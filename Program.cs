using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddSingleton<InMemoryRepository>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.MapGet("/", () => Results.Redirect("/swagger"));

// --- FLIGHTS ---
app.MapGet("/flights", (InMemoryRepository repo) => Results.Ok(repo.Flights));

app.MapGet("/flights/{id:guid}", (InMemoryRepository repo, Guid id) =>
{
    var f = repo.Flights.FirstOrDefault(x => x.Id == id);
    return f is null ? Results.NotFound() : Results.Ok(f);
});

app.MapGet("/flights/search", (InMemoryRepository repo, string from, string to, DateTime? date) =>
{
    var q = repo.Flights.AsQueryable()
        .Where(f => f.DepartureCity.Equals(from, StringComparison.OrdinalIgnoreCase)
                 && f.ArrivalCity.Equals(to, StringComparison.OrdinalIgnoreCase));
    if (date.HasValue)
    {
        var d = date.Value.Date;
        q = q.Where(f => f.DepartureDate.Date == d);
    }
    return Results.Ok(q.ToList());
});

app.MapPost("/flights", (InMemoryRepository repo, FlightCreateDto dto) =>
{
    var f = new Flight
    {
        Id = Guid.NewGuid(),
        FlightNumber = dto.FlightNumber,
        DepartureCity = dto.DepartureCity,
        ArrivalCity = dto.ArrivalCity,
        DepartureDate = dto.DepartureDate,
        Price = dto.Price,
        SeatsTotal = dto.SeatsTotal,
        SeatsAvailable = dto.SeatsTotal
    };
    repo.Flights.Add(f);
    return Results.Created($"/flights/{f.Id}", f);
});

// --- PASSENGERS ---
app.MapGet("/passengers", (InMemoryRepository repo) => Results.Ok(repo.Passengers));

app.MapPost("/passengers", (InMemoryRepository repo, PassengerCreateDto dto) =>
{
    var p = new Passenger
    {
        Id = Guid.NewGuid(),
        FullName = dto.FullName,
        Email = dto.Email,
        Phone = dto.Phone
    };
    repo.Passengers.Add(p);
    return Results.Created($"/passengers/{p.Id}", p);
});

// --- TICKETS ---
app.MapPost("/tickets", (InMemoryRepository repo, TicketCreateDto dto) =>
{
    var flight = repo.Flights.FirstOrDefault(f => f.Id == dto.FlightId);
    if (flight is null) return Results.BadRequest($"Flight {dto.FlightId} not found.");
    if (flight.SeatsAvailable <= 0) return Results.BadRequest("No seats available on this flight.");

    var passenger = repo.Passengers.FirstOrDefault(p => p.Id == dto.PassengerId);
    if (passenger is null) return Results.BadRequest($"Passenger {dto.PassengerId} not found.");

    var ticket = new Ticket
    {
        Id = Guid.NewGuid(),
        FlightId = flight.Id,
        PassengerId = passenger.Id,
        Price = flight.Price,
        SeatNumber = $"S{flight.SeatsTotal - flight.SeatsAvailable + 1}",
        BookingDate = DateTime.UtcNow
    };

    flight.SeatsAvailable--;
    repo.Tickets.Add(ticket);
    return Results.Created($"/tickets/{ticket.Id}", ticket);
});

app.MapGet("/tickets/{id:guid}", (InMemoryRepository repo, Guid id) =>
{
    var t = repo.Tickets.FirstOrDefault(x => x.Id == id);
    return t is null ? Results.NotFound() : Results.Ok(t);
});

app.MapGet("/tickets", (InMemoryRepository repo) => Results.Ok(repo.Tickets));

app.Run();

public record FlightCreateDto(string FlightNumber, string DepartureCity, string ArrivalCity, DateTime DepartureDate, decimal Price, int SeatsTotal);
public record PassengerCreateDto(string FullName, string Email, string? Phone);
public record TicketCreateDto(Guid FlightId, Guid PassengerId);

public class Flight
{
    public Guid Id { get; set; }
    public string FlightNumber { get; set; } = default!;
    public string DepartureCity { get; set; } = default!;
    public string ArrivalCity { get; set; } = default!;
    public DateTime DepartureDate { get; set; }
    public decimal Price { get; set; }
    public int SeatsTotal { get; set; }
    public int SeatsAvailable { get; set; }
}

public class Passenger
{
    public Guid Id { get; set; }
    public string FullName { get; set; } = default!;
    public string Email { get; set; } = default!;
    public string? Phone { get; set; }
}

public class Ticket
{
    public Guid Id { get; set; }
    public Guid FlightId { get; set; }
    public Guid PassengerId { get; set; }
    public decimal Price { get; set; }
    public string SeatNumber { get; set; } = default!;
    public DateTime BookingDate { get; set; }
}

public class InMemoryRepository
{
    public List<Flight> Flights { get; } = new();
    public List<Passenger> Passengers { get; } = new();
    public List<Ticket> Tickets { get; } = new();

    public InMemoryRepository()
    {
        Flights.AddRange(new[]
        {
            new Flight {
                Id = Guid.NewGuid(),
                FlightNumber = "KC101",
                DepartureCity = "Almaty",
                ArrivalCity = "Nur-Sultan",
                DepartureDate = DateTime.Today.AddDays(1).AddHours(8),
                Price = 120.50m,
                SeatsTotal = 100,
                SeatsAvailable = 100
            },
            new Flight {
                Id = Guid.NewGuid(),
                FlightNumber = "KC202",
                DepartureCity = "Almaty",
                ArrivalCity = "Istanbul",
                DepartureDate = DateTime.Today.AddDays(2).AddHours(14),
                Price = 320.00m,
                SeatsTotal = 180,
                SeatsAvailable = 50
            },
            new Flight {
                Id = Guid.NewGuid(),
                FlightNumber = "KC303",
                DepartureCity = "Almaty",
                ArrivalCity = "Aktobe",
                DepartureDate = DateTime.Today.AddDays(1).AddHours(10),
                Price = 80.00m,
                SeatsTotal = 50,
                SeatsAvailable = 20
            }
        });

        Passengers.AddRange(new[]
        {
            new Passenger { Id = Guid.NewGuid(), FullName = "Aibek K.", Email = "aibek@example.com", Phone = "+7-700-000000" },
            new Passenger { Id = Guid.NewGuid(), FullName = "Dina S.", Email = "dina@example.com", Phone = "+7-701-111111" }
        });
    }
}
